#coding=utf-8
from evennia import DefaultCharacter
from evennia import TICKER_HANDLER
from evennia import logger
from evennia import search_object
from evennia import create_object
import random

from commands.default_cmdsets import CharacterCmdSet
from settings.masterdef.huashanmasters import HuaShanMaster
from utils.general import determine_one_hit


class Master(DefaultCharacter):

    DEFINITION = HuaShanMaster.GAOGENMING

    def at_init(self):
        """
        When initialized from cache (after a server reboot), set up
        the AI state.
        """
        # The AI state machine (not persistent).
        self.ndb.is_immortal = self.db.immortal or self.db.is_dead
        self.ndb.is_attacking = False
        self.ndb.is_idle = True

    def at_object_creation(self):
        super(Master, self).at_object_creation()
        self.cmdset.add(CharacterCmdSet, permanent=True)

        # 姓名，等级
        self.db.gender = self.DEFINITION.get("gender")
        self.db.name = self.DEFINITION.get("name")
        self.db.rank = self.DEFINITION.get("rank")
        # 技能和技能上限等级
        self.db.skills = self.DEFINITION.get("skills")
        self.db.skill_level = self.DEFINITION.get("skill_level")

        # 伤害，防御，攻击速度，命中，暴击率，躲闪，招架
        self.db.damage = self.DEFINITION.get("damage")
        self.db.defend = self.DEFINITION.get("defend")
        self.db.attack_speed = self.DEFINITION.get("attack_speed")
        self.db.critical_hit = self.DEFINITION.get("critical_hit")
        self.db.parry = self.DEFINITION.get("parry")
        self.db.avoid = self.DEFINITION.get("avoid")
        self.db.hit = self.DEFINITION.get("hit")

        # 生命值, 内力
        self.db.full_health = self.DEFINITION.get("full_health")
        self.db.full_energy = self.DEFINITION.get("full_energy")

        # 人物的当前状态
        self.db.is_dead = self.DEFINITION.get("is_dead")
        self.db.immortal = self.DEFINITION.get("immortal")

        # 可掉落的物品 和寻宝几率
        self.db.available_drop_items = self.DEFINITION.get("available_drop_items")
        self.db.drop_rate = self.DEFINITION.get("magic_found")

        # 当前状态
        self.db.current_enemy = None
        self.db.health = self.db.full_health
        self.db.energy = self.db.full_energy
        # 掉落的物品存放在此
        self.db.drop_item_list = []

        # 最后一次定时器的间隔和方法
        self.db.last_ticker_interval = None
        self.db.last_hook_key = None

        #  根据skill_list生成对象的技能列表
        self.generate_skills()

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
        text = super(Master, self).return_appearance(looker)
        cscore = "(性别: %s 等级: %s 气血: %s/%s 内力: %s/%s\n" % \
                 (self.db.gender, str(self.db.rank.get("name")), self.db.health, self.db.full_health, self.db.energy, self.db.full_energy)
        cscore += "攻击: %s  命中: %s 攻速: %s 暴击: %s 防御: %s  躲闪: %s 招架: %s\n" % \
                  (self.db.damage, self.db.hit, self.db.attack_speed, self.db.critical_hit, self.db.defend, self.db.avoid, self.db.parry)

        for skill in self.db.skill_list:
            cscore += (skill.db.name + " " + str(skill.db.level) + "级/"+skill.db.level_desc + "\n")
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
        # # 敌方伤害值
        # damage_taken = attacker.db.damage
        # # 是否命中标志
        # binggo = False
        # rate = 0.00
        # # 判定是否招架成功, 命中几率为命中除以两倍的招架
        # rate = attacker.db.hit/float(self.db.parry)/2.00
        # if random.random() < rate:
        #     # 判定是否躲闪成功，命中几率为命中除以两倍的躲闪
        #     rate = attacker.db.hit / float(self.db.avoid) / 2.00
        #     if random.random() < rate:
        #         binggo = True
        #     else:
        #         attacker.msg("你的攻击被 %s 躲闪" % self.key)
        #         self.msg("你躲闪了 %s 的攻击" % (attacker.key))
        # else:
        #     attacker.msg("你的攻击被 %s 格挡" % self.key)
        #     self.msg("你格挡了 %s 的攻击" % (attacker.key))
        #
        # # 如果命中，则减去自身防御值后为最终伤害
        # is_critical = False
        # if binggo:
        #     # 判断敌方是否暴击，如暴击则伤害加倍
        #     if random.random() < attacker.db.critical_hit:
        #         damage_taken *= 2
        #         is_critical = True
        #     # 减去自身防御
        #     damage_taken -= self.db.defend
        #     if damage_taken > 0:
        #         self.db.health -= damage_taken
        #         if is_critical:
        #             attacker.msg("你对 %s 造成了 %s 点暴击伤害" % (self.key, damage_taken))
        #             self.msg("%s 对你造成了 %s 点暴击伤害" % (attacker.key, damage_taken))
        #         else:
        #             attacker.msg("你对 %s 造成了 %s 点伤害" % (self.key, damage_taken))
        #             self.msg("%s 对你造成了 %s 点伤害" % (attacker.key, damage_taken))
        #     else:
        #         attacker.msg("你的攻击未能对 %s 造成任何伤害" % self.key)
        #         self.msg("%s 的攻击未对你造成任何伤害" % attacker.key)
        #
        # if self.db.health <= 0:
        #     self.location.msg_contents("%s 重重倒下了" % self.key, exclude=self)
        #     self.msg("你已经死亡")
        #     attacker.msg("%s 已经死亡" % self.key)
        #     self.set_dead()
        # else:
        #     if not self.ndb.is_attacking:
        #         self.db.current_enemy = attacker
        #         attacker.msg("%s 开始对你发起攻击" % self.key)
        #         self.start_attacking()

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
                self.execute_cmd("%s %s" % (cmd_string, target))
        else:
            self.start_idle()

    def start_attacking(self):
        self.ndb.is_attacking = True
        self._set_ticker(self.db.attack_speed, "do_attack")

    def start_idle(self):
        """
        Starts just standing around. This will kill
        the ticker and do nothing more.
        """
        self.ndb.is_attacking = False
        self._set_ticker(None, None, stop=True)

    def set_dead(self):
        self.db.is_dead = True
        self.ndb.is_attacking = False
        self.ndb.is_immortal = True
        self.db.desc = self.key + "的尸体"
        self.drop_objects()
        self._set_ticker(self.db.reborn_interval, "set_alive")


    def set_alive(self):
        self.db.is_dead = False
        self.ndb.is_attacking = False
        self.ndb.is_immortal = self.db.immortal
        self.db.health = self.db.full_health
        self.db.energy = self.db.full_energy
        self.db.desc = self.key
        self.db.drop_item_list = []
        if not self.location:
            self.move_to(self.home)
        self.start_idle()

    def drop_objects(self):
        self.db.drop_item_list.append(random.choice(self.db.available_drop_items))

    # 此方法在npc被创建是调用，生成该NPC技能列表和等级
    def generate_skills(self):
        self.db.skill_list = []
        for skill in self.db.skills:
            skill_created = create_object(skill.get("classpath"),
                                         key=skill.get("name"),
                                         location=self,
                                         locks="edit:id(%i) and perm(Builders);call:id(%i)" % (
                                         self.id, self.id))
            skill_created.levels_up(self, self.db.skill_level)
            self.db.skill_list.append(skill_created)

