#coding=utf-8
"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from evennia import DefaultCharacter
from evennia import TICKER_HANDLER
from evennia import logger
from evennia import search_object
from evennia import create_object
import random

from commands.default_cmdsets import CharacterCmdSet
from settings import rank
from settings.general import Gender, Color
from settings.level_exp import exp_dict
from settings.rank import apprentice
from utils import general
from utils.general import determine_one_hit, show_me_the_money


class Character(DefaultCharacter):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_after_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(account) -  when Account disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Account has disconnected"
                    to the room.
    at_pre_puppet - Just before Account re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "AccountName has entered the game" to the room.

    """
    GENDER = Gender.MALE
    RANK = apprentice
    BASE_ATTACK_SPEED = 4

    def at_init(self):
        """
        When initialized from cache (after a server reboot), set up
        the AI state.
        """
        # The AI state machine (not persistent).
        self.ndb.is_immortal = self.db.immortal or self.db.is_dead
        self.ndb.is_attacking = False
        self.ndb.is_minning = False
        self.ndb.is_studying = False
        self.ndb.is_practising = False
        self.ndb.is_idle = False

    def at_object_creation(self):
        self.cmdset.add(CharacterCmdSet, permanent=True)

        # 姓名，等级
        self.db.gender = self.GENDER
        self.db.rank = self.RANK
        self.db.level = 1

        # 经验， 潜能，精力
        self.db.experience = 1000
        self.db.potential = 1000
        self.db.vigor = 100

        # 臂力，身法，根骨，悟性
        # 1 身法 = 0.5 命中 0.5躲闪0.1暴击率 0.004攻速
        # 1 臂力 = 1攻击 0.5招架
        # 1 根骨 = 5 生命 0.25防御
        self.db.strength = 30
        self.db.agility = 15
        self.db.stamina = 20
        self.db.smart = 15
        self.db.magic_found = 20

        # 伤害，防御，攻击速度，命中，暴击率，躲闪，招架
        self.db.damage = self.db.strength
        self.db.defend = self.db.stamina * 0.25
        self.db.attack_speed = self.BASE_ATTACK_SPEED - self.db.agility*0.004
        self.db.critical_hit = 0.1 * self.db.agility/100.00
        self.db.avoid = 0.5 * self.db.agility
        self.db.parry = 0.5 * self.db.strength
        self.db.hit = 0.5 * self.db.agility

        # 生命值, 内力
        self.db.full_health = self.db.stamina * 5
        self.db.health = self.db.full_health
        self.db.full_energy = 100
        self.db.energy = self.db.full_energy

        # 金钱
        self.db.money = 0

        # 人物的状态
        self.db.is_dead = False
        self.db.immortal = False

        # 当前敌人
        self.db.current_enemy = None

        # 死亡后被传送的地方
        self.db.send_defeated_to = "darkcell"

        # 最后一次定时器的间隔和方法
        self.db.last_ticker_interval = None
        self.db.last_hook_key = None

    def get_abilities(self):
        """
        Simple access method to return ability
        scores as a tuple (str,agi,mag)
        """
        return self.db.level, self.db.strength, self.db.agility, self.db.stamina, self.db.health

    def return_appearance(self, looker):
        """
        The return from this method is what
        looker sees when looking at this object.
        """
        text = super(Character, self).return_appearance(looker)
        cscore = "(性别: %s 等级: %s 经验: %s 潜能: %s\n" \
                 "气血: %s/%s 内力: %s/%s 精力: %s\n" % \
                 (self.db.gender, str(self.db.rank.get("name")),self.db.experience,self.db.potential,
                  self.db.health, self.db.full_health, self.db.energy, self.db.full_energy, self.db.vigor)
        cscore += "臂力: %s 身法: %s 根骨: %s 悟性: %s 福缘: %s\n" \
                  "攻击: %s  命中: %s 攻速: %s 暴击: %s\n" \
                  "防御: %s  躲闪: %s 招架: %s)" % \
                  (self.db.strength, self.db.agility, self.db.stamina, self.db.smart,self.db.magic_found,
                   self.db.damage, self.db.hit, self.db.attack_speed, self.db.critical_hit,
                   self.db.defend, self.db.avoid, self.db.parry)
        if "\n" in text:
            # text is multi-line, add score after first line
            first_line, rest = text.split("\n", 1)
            # text = first_line + cscore + "\n" + rest
            text = first_line + cscore + "\n"
        else:
            # text is only one line; add score to end
            text += cscore
        return text

    def _set_ticker(self, interval, hook_key, stop=False):
        """
        Set how often the given hook key should
        be "ticked".

        Args:
            interval (int): The number of seconds
                between ticks
            hook_key (str): The name of the method
                (on this mob) to call every interval
                seconds.
            stop (bool, optional): Just stop the
                last ticker without starting a new one.
                With this set, the interval and hook_key
                arguments are unused.

        In order to only have one ticker
        running at a time, we make sure to store the
        previous ticker subscription so that we can
        easily find and stop it before setting a
        new one. The tickerhandler is persistent so
        we need to remember this across reloads.

        """
        idstring = "ticker_string"  # this doesn't change
        last_interval = self.db.last_ticker_interval
        last_hook_key = self.db.last_hook_key
        if last_interval and last_hook_key:
             # we have a previous subscription, kill this first.
            TICKER_HANDLER.remove(interval=last_interval,
                                  callback=getattr(self, last_hook_key), idstring=idstring)
        self.db.last_ticker_interval = interval
        self.db.last_hook_key = hook_key
        if not stop:
            TICKER_HANDLER.add(interval=interval,
                               callback=getattr(self, hook_key), idstring=idstring)

    def _set_study_ticker(self, interval, hook_key, stop=False, skill=None, master=None):
        """
        Set how often the given hook key should
        be "ticked".

        Args:
            interval (int): The number of seconds
                between ticks
            hook_key (str): The name of the method
                (on this mob) to call every interval
                seconds.
            stop (bool, optional): Just stop the
                last ticker without starting a new one.
                With this set, the interval and hook_key
                arguments are unused.

        In order to only have one ticker
        running at a time, we make sure to store the
        previous ticker subscription so that we can
        easily find and stop it before setting a
        new one. The tickerhandler is persistent so
        we need to remember this across reloads.

        """
        idstring = "ticker_string"  # this doesn't change
        last_interval = self.db.last_ticker_interval
        last_hook_key = self.db.last_hook_key
        if last_interval and last_hook_key:
             # we have a previous subscription, kill this first.
            TICKER_HANDLER.remove(interval=last_interval,
                                  callback=getattr(self, last_hook_key), idstring=idstring)
        self.db.last_ticker_interval = interval
        self.db.last_hook_key = hook_key
        if not stop:
            # set the new ticker
            TICKER_HANDLER.add(interval, getattr(self, hook_key), idstring, True, skill, master)

    def _set_practise_ticker(self, interval, hook_key, stop=False, skill=None):
        """
        Set how often the given hook key should
        be "ticked".

        Args:
            interval (int): The number of seconds
                between ticks
            hook_key (str): The name of the method
                (on this mob) to call every interval
                seconds.
            stop (bool, optional): Just stop the
                last ticker without starting a new one.
                With this set, the interval and hook_key
                arguments are unused.

        In order to only have one ticker
        running at a time, we make sure to store the
        previous ticker subscription so that we can
        easily find and stop it before setting a
        new one. The tickerhandler is persistent so
        we need to remember this across reloads.

        """
        idstring = "ticker_string"  # this doesn't change
        last_interval = self.db.last_ticker_interval
        last_hook_key = self.db.last_hook_key
        if last_interval and last_hook_key:
             # we have a previous subscription, kill this first.
            TICKER_HANDLER.remove(interval=last_interval,
                                  callback=getattr(self, last_hook_key), idstring=idstring)
        self.db.last_ticker_interval = interval
        self.db.last_hook_key = hook_key
        if not stop:
            # set the new ticker
            TICKER_HANDLER.add(interval, getattr(self, hook_key), idstring, True, skill)

    def _find_target(self, location):
        """
        Scan the given location for suitable targets (this is defined
        as Characters) to attack.  Will ignore superusers.

        Args:
            location (Object): the room to scan.

        Returns:
            The first suitable target found.

        """
        targets = [obj for obj in location.contents_get(exclude=self)
                   if obj.has_account and not obj.is_superuser]
        return targets[0] if targets else None

    def at_hit(self, attacker):
        determine_one_hit(self, attacker)

        if self.db.health <= 0:
            self.location.msg_contents("%s 重重倒下了" % self.key, exclude=self)
            self.msg("你已经死亡")
            attacker.msg("%s 已经死亡" % self.key)
            # attacker.gain_exp(self.db.exp_when_killed, self.db.exp_when_killed)
            # attacker.gain_money(self.db.money_when_killed)
            self.set_dead()
        else:
            if not self.ndb.is_attacking:
                self.db.current_enemy = attacker
                attacker.msg("%s 开始对你发起攻击" % self.key)
                self.start_attacking()

    def do_attack(self):
        cmd_string = "attack"
        # 判断是否已有敌人目标而且目标是否在自己房间内，否则在房间内搜索任意敌人并发动攻击，如果都没有找到，则恢复为不动状态
        if self.db.current_enemy and self.db.current_enemy in self.location.contents_get(exclude=self):
            target = self.db.current_enemy
        else:
            # self.db.current_enemy = self._find_target(self.location)
            # target = self.db.current_enemy
            self.msg("你要攻击谁？")
            self.start_idle()

        if target:
            if (target.db.health <= 0):
                self.start_idle()
            else:
                # self.execute_cmd("%s %s" % (cmd_string, target))
                target.at_hit(self)
        else:
            self.start_idle()

    def start_attacking(self):
        self.ndb.is_attacking = True
        self.do_attack()
        self._set_ticker(self.db.attack_speed, "do_attack")

    def do_practise(self, skill):
        # 当潜能>0, 所学习的技能等级小于自身等级时，容许学习
        # 对特殊武学，还需加上判断：特殊武学的级别小于基础武学的级别
        if self.db.potential > 1000:
            if skill.db.level < self.db.level:
                #  这里用level_up方法而不是用 level+1, 因为level_up方法除了level+1,还会把技能的升级后的影响附加到人物身上
                skill.level_up(self)
                self.db.potential -= 1000
                self.msg("你对%s似乎有所体会" % skill.db.name)
                self.msg("你的%s等级提升了!!!" % skill.db.name)
                self.msg("你正在学习%s" % skill.db.name)
            else:
                self.msg("你对%s总是无法进一步理解，似乎需要更多的实战经验" % skill.db.name)
                self.start_idle()
        else:
            self.msg("你的潜能不够了")
            self.start_idle()

    def start_pracising(self, skill):
        self.msg("你正在练习%s" % skill.db.name)
        self.ndb.is_practising = True
        self._set_practise_ticker(10, "do_practise", skill=skill)

    def do_study(self, skill, master):
        # 当潜能>0, 所学习的技能等级小于师傅的技能等级，所学习的技能等级小于自身等级时，容许学习
        # 对特殊武学，还需加上判断：特殊武学的级别小于基础武学的级别
        if self.db.potential > 1000:
            if skill.db.level < master.db.skill_level:
                if skill.db.level < self.db.level:
                    #  这里用level_up方法而不是用 level+1, 因为level_up方法除了level+1,还会把技能的升级后的影响附加到人物身上
                    skill.level_up(self)
                    self.db.potential -= 1000
                    self.msg("你对%s似乎有所体会" % skill.db.name)
                    self.msg("你的%s等级提升了!!!" % skill.db.name)
                    self.msg("你正在学习%s" % skill.db.name)
                else:
                    self.msg("你对师傅的讲解总是无法理解，似乎需要更多的实战经验")
                    self.start_idle()
            else:
                self.msg("你对%s的理解已经不下于师傅了" % skill.db.name)
                self.start_idle()
        else:
            self.msg("你的潜能不够了")
            self.start_idle()

    def start_studying(self, skill, master):
        self.msg("你正在学习%s" % skill.db.name)
        self.ndb.is_studying = True
        self._set_study_ticker(5, "do_study", skill=skill, master=master)

    def start_idle(self):
        """
        Starts just standing around. This will kill
        the ticker and do nothing more.
        """
        self.ndb.is_attacking = False
        self.ndb.is_minning = False
        self.ndb.is_studying = False
        self.ndb.is_practising = False
        self._set_ticker(None, None, stop=True)

    def set_dead(self):
        self.db.is_dead = True
        self.ndb.is_attacking = False
        self.ndb.is_immortal = True
        send_defeated_to = search_object(self.db.send_defeated_to)
        if send_defeated_to:
            self.move_to(send_defeated_to[0], quiet=True)
        else:
            self.msg(send_defeated_to + " 未找到")
            logger.log_err("Mob: mob.db.send_defeated_to not found: %s" % self.db.send_defeated_to)
        self.set_alive()

    def set_alive(self):
        self.db.is_dead = False
        self.ndb.is_attacking = False
        self.ndb.is_immortal = self.db.immortal
        self.db.health = self.db.full_health
        if not self.location:
            self.move_to(self.home)

    def gain_exp(self, exp, potential):
        if exp and potential:
            self.msg("你获得了%s点经验 %s点潜能" % (exp, potential))
            self.db.experience += exp
            self.db.potential += potential

    def gain_money(self, money):
        if money:
            self.msg("你获得了%s" % show_me_the_money(money))
            self.db.money += money

    def rank_up(self):
        index = rank.rank_list.index(self.db.rank)
        try:
            self.db.rank = rank.rank_list[index + 1]
            self.msg("恭喜你升到了%s" % self.db.rank["name"])
            self.db.full_energy += 1000
            self.db.max_skill_level += 100
        except:
            self.msg("你已经是最高级别了，还想升级啊")

    def start_mining(self):
        self.ndb.is_minning = True
        self._set_ticker(5, "do_mine")

    def do_mine(self):
        self.gain_exp(self.db.rank.get("exp"),self.db.rank.get("potential"))

    def get_skill_level(self, exp):
        self._set_skill_level()
        return self.db.skill_level

    def _set_skill_level(self):
        for level in exp_dict.keys()[22]:
            exp = exp_dict.get(level)
            if self.db.experience > exp:
                continue
            else:
                self.db.skill_level = level
                return
        self.msg("已达到技能等级上限")

    # 以下这些命令是改变人物属性，如果改变的是基础属性的话同时相应的改变战斗属性
    def add_strength(self, point):
        self.db.strength += point
        self.db.damage += point
        self.db.parry += 0.5 * point

    def add_agility(self, point):
        self.db.agility += point
        self.db.hit += 0.5 * point
        self.db.avoid += 0.5 * point
        self.db.critical_hit += 0.1 * point/100.00
        self.db.attack_speed -= 0.004 * point

    def add_stamina(self, point):
        self.db.stamina += point
        self.db.full_health += 5 * point
        self.db.defend += 0.25 * point

    def add_smart(self, point):
        self.db.smart += point

    def add_damage(self, point):
        self.db.damage += point

    def add_attack_speed(self, point):
        self.db.attack_speed -= point/100.00

    def add_critical_hit(self, point):
        self.db.critical_hit += point/100.00

    def add_hit(self, point):
        self.db.hit += point

    def add_avoid(self, point):
        self.db.avoid += point

    def add_parry(self, point):
        self.db.parry += point

    def add_defend(self, point):
        self.db.defend += point


    # def is_busy(self):
    #     self.ndb.is_busy = self.ndb.is_attacking or self.ndb.is_minning or self.ndb.is_studying or self.ndb.is_practising
    #     return self.ndb.is_busy

    # def level_up(self):
    #     self.db.level += 1
    #     self.msg("恭喜，你升到了%s级" % self.db.level)
    #
    #     self.db.strength += 1
    #     self.db.agility += 1
    #     self.db.stamina += 1
    #     self.msg("你的力量提升了1点")
    #     self.msg("你的敏捷提升了1点")
    #     self.msg("你的耐力提升了1点")
    #
    #     #TODO: 添加代码根据属性的变化改变其他属性
    #
    # def set_strength(self, number):
    #     self.db.strength += number
    #     #TODO: 力量变动导致伤害变动
    #
    # def set_agility(self, number):
    #     self.db.agility += number
    #     # TODO: 敏捷变动导致躲闪，攻速和暴击变动
    #
    # def set_stamina(self, number):
    #     self.db.stamina += number
    #     # TODO: 耐力变动导致最大生命值变动