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
from evennia import search_object
from evennia import create_object
from evennia import logger
from commands.default_cmdsets import MonsterCmdSet

import random


class Monster(DefaultCharacter):
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
    BASE_MAGIC_FOUND = 0.99

    def at_init(self):
        """
        When initialized from cache (after a server reboot), set up
        the AI state.
        """
        # The AI state machine (not persistent).
        self.ndb.is_attacking = False
        self.ndb.is_immortal = self.db.immortal or self.db.is_dead

    def at_object_creation(self):
        """
        字段解释：
            level 等级（每级增加1点属性点）
            experience 经验（决定等级）
            strength 力量（决定伤害）
            agility 敏捷（决定攻击速度，暴击率，躲闪）
            stamina 体力（决定最大生命值）
            damage 伤害（由属性和装备决定）
            defence 防御（由属性和装备决定）
            attack_speed 攻击速度（由属性和装备决定）
            critical_strike_hit 暴击几率（由属性和装备决定）
            full_health 最大生命值 (由属性和装备决定)
            health 当前生命值
            is_dead 是否处于死亡状态
            engaged_in_combat 是否处于战斗状态
        """
        self.cmdset.add(MonsterCmdSet, permanent=True)

        self.db.level = 1
        self.db.exp_when_killed = 1000

        self.db.strength = 10
        self.db.agility = 10
        self.db.stamina = 10

        self.db.damage = 10
        self.db.defend = 1
        self.db.attack_speed = 6
        self.db.critical_strike_hit = 0.01
        self.db.full_health = 1000
        self.db.health = self.db.full_health

        # 怪物状态
        self.db.is_dead = False
        self.db.immortal = False

        # 重生时间间隔
        self.db.reborn_interval = 300

        # 当前敌人
        self.db.current_enemy = None

        # 死亡消息
        self.db.defeat_msg = "You fall to the ground."
        self.db.defeat_msg_room = "%s falls to the ground."

        # 最后一次定时器间隔和hook key
        self.db.last_ticker_interval = None
        self.db.last_hook_key = None

        # 掉落的物品存放在此
        self.db.drop_item_list = []
        # 可掉落的物品
        self.db.available_drop_items = ["Longsword"]
        # 掉落物品品质几率
        self.db.drop_rate = self.BASE_MAGIC_FOUND

    def return_appearance(self, looker):
        """
        The return from this method is what
        looker sees when looking at this object.
        """
        text = super(Monster, self).return_appearance(looker)
        cscore = " (等级: %s, 力量: %s, 敏捷: %s, 耐力: %s, 生命值: %s/%s\n 攻击：%s 防御：%s 攻速：%s)" % \
                 ( self.db.level, self.db.strength, self.db.agility, self.db.stamina, self.db.health, self.db.full_health,
                   self.db.damage, self.db.defend, self.db.attack_speed)
        if "\n" in text:
            # text is multi-line, add score after first line
            first_line, rest = text.split("\n", 1)
            text = first_line + cscore + "\n" + rest
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
            # set the new ticker
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
        damage_taken = attacker.db.damage
        self.db.health -= damage_taken
        attacker.msg("你对 %s 造成了 %s 点伤害" % (self.key, damage_taken))
        self.msg("%s 对你造成了 %s 点伤害" % (attacker.key, damage_taken))
        if self.db.health <= 0:
            self.location.msg_contents("%s 重重倒下了" % self.key, exclude=self)
            self.msg("你已经死亡")
            attacker.msg("%s 已经死亡" % self.key)
            attacker.gain_exp(self.db.exp_when_killed)
            self.set_dead()
        else:
            if not self.ndb.is_attacking:
                self.db.current_enemy = attacker
                attacker.msg("%s 锁定你为敌人，开始攻击你" % self.key)
                self.start_attacking()


    def do_attack(self):
        # 解决定时器延时问题：在自身死亡后因为定时器延时触发，还会再攻击对方一次
        if self.db.is_dead:
            return
        cmd_string = "attack"
        # 判断是否已有敌人目标而且目标是否在自己房间内，否则在房间内搜索任意敌人并发动攻击，如果都没有找到，则恢复为不动状态
        if self.db.current_enemy and self.db.current_enemy in self.location.contents_get(exclude=self):
            target = self.db.current_enemy
        else:
            self.db.current_enemy = self._find_target(self.location)
            target = self.db.current_enemy

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
        self.db.desc = "a dead body"
        self.drop_objects()
        self._set_ticker(self.db.reborn_interval, "set_alive")


    def set_alive(self):
        self.db.is_dead = False
        self.ndb.is_attacking = False
        self.ndb.is_immortal = self.db.immortal
        self.db.health = self.db.full_health
        self.db.desc = "a walking ghost"
        self.db.drop_item_list = []
        if not self.location:
            self.move_to(self.home)

    def drop_objects(self):
        self.db.drop_item_list.append(random.choice(self.db.available_drop_items))
