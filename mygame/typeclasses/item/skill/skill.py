#coding=utf-8
import commands
from evennia import TICKER_HANDLER

from settings.skilldef import SkillDefinition, SkillDesc
from typeclasses.objects import Object
from utils.equiputil import at_equip_skill

class Skill(Object):
    """
    为什么技能是物品：
    1. 可以从caller.contents得到所有物品，然后用isinstance(Skill)得到所有的物品
    2. 可以加上命令集
    """
    DEFINITION = SkillDefinition.BASE_QUANJIAO

    def at_object_creation(self):
        super(Skill, self).at_object_creation()
        self.cmdset.add(commands.default_cmdsets.SkillCmdSet, permanent=True)
        self.db.is_equiped = False

        self.db.color = self.DEFINITION.get("color")
        self.db.name = self.DEFINITION.get("name")
        self.db.type = self.DEFINITION.get("category")
        self.db.cooldown_time = self.DEFINITION.get("cooldown")
        self.db.classpath = self.DEFINITION.get("classpath")

        self.db.is_ready = True
        self.db.level = 0
        self.db.level_desc = self.get_level_desc()

        # 技能对人物属性点的加点
        self.db.strength_points = 0
        self.db.agility_points = 0
        self.db.stamina_points = 0
        self.db.smart_points = 0

        # 技能对人物战斗属性的加成
        self.db.damage_points = 0
        self.db.defend_points = 0
        self.db.attack_speed_points = 0
        self.db.critical_hit_points = 0
        self.db.avoid_points = 0
        self.db.parry_points = 0
        self.db.hit_points = 0

        # 最后一次定时器的间隔和方法
        self.db.last_ticker_interval = None
        self.db.last_hook_key = None

    def return_appearance(self, looker):
        """
        The return from this method is what
        looker sees when looking at this object.
        """
        self.set_words()
        text = super(Skill, self).return_appearance(looker)
        cscore = "等级: %s (%s)" % (self.db.level, self.db.color) + "\n"  + \
                 "  伤害: %s" % self.db.damage_points + "\n" + \
                 "  臂力 + %s" % self.db.strength_points + "\n" + \
                 "  身法 + %s" % self.db.agility_points + "\n" + \
                 "  根骨 + %s" % self.db.stamina_points + "\n" + \
                 "  悟性 + %s" % self.db.smart_points + "\n" + \
                 "  防御 + %s" % self.db.defend_points + "\n" + \
                 "  攻速 + %s" % (self.db.attack_speed_points/100.00) + "\n" + \
                 "  暴击率 + %s" % (self.db.critical_hit_points/100.00) + "\n" + \
                 "  躲闪 + %s" % self.db.avoid_points + "\n" + \
                 "  招架 + %s" % self.db.parry_points + "\n" + \
                 "  命中 + %s" % self.db.hit_points + "\n"
        if "\n" in text:
            # text is multi-line, add score after first line
            first_line, rest = text.split("\n", 1)
            text = first_line + cscore + "\n" + rest
        else:
            # text is only one line; add score to end
            text += cscore
        return text

    # 定义技能属性
    def set_words(self):
        pass

    # 施放技能所带的招数
    def cast(self, caller, target):
        pass

    def do_cooldown(self):
        self.db.is_ready = True
        self._set_ticker(None, None, stop=True)

    def start_cooldown(self):
        self._set_ticker(self.db.cooldown_time, "do_cooldown")

    def get_level_desc(self):
        if (self.db.level < 100):
            return SkillDesc.CHU_XUE_ZHA_LIAN
        if (self.db.level < 200):
            return SkillDesc.CHU_TONG_PI_MAO
        if (self.db.level < 300):
            return SkillDesc.BAN_SHENG_BU_SHU
        if (self.db.level < 400):
            return SkillDesc.MA_MA_HU_HU
        if (self.db.level < 500):
            return SkillDesc.PING_DAN_WU_QI
        if (self.db.level < 800):
            return SkillDesc.JIA_QING_JIU_SHU
        if (self.db.level < 1000):
            return SkillDesc.CHU_RU_JIA_JING
        if (self.db.level < 1200):
            return SkillDesc.XIN_LING_SHEN_HUI
        if (self.db.level < 1500):
            return SkillDesc.CHAO_QUN_JUE_LUN
        if (self.db.level < 10000):
            return SkillDesc.CHAO_FNA_RU_SHENG

    def level_up(self, caller):
        # 如果未装备，则技能升级
        if not self.db.is_equiped:
            self.db.level += 1
            self.set_words()
        # 如果已经装备，则先卸下技能，技能升级，再装上技能。以显示实时变化
        else:
            self.at_equip(caller, equip=False)
            self.db.level += 1
            self.set_words()
            self.at_equip(caller, equip=True)

    def levels_up(self, caller, levels):
        for i in range(self.db.level, levels):
            self.level_up(caller)

    def at_equip(self, caller, equip=True):
        """
        装备上物品，并把装备上的属性添加到人物身上。
        当 reverse=True 的时候把装备上的属性从人物身上取消。
        :param caller: 人物，命令调用者
        :param self: 装备物品
        :param reverse: 开关，控制装备或者脱下
        :return: 无
        """
        self.set_words()
        at_equip_skill(self, caller, equip=equip)
        # if reverse:
        #     self.db.is_equiped = False
        #     if self.db.strength_points:
        #         if hasattr(caller, "add_strength"):
        #             caller.add_strength(-self.db.strength_points)
        #     if self.db.agility_points:
        #         if hasattr(caller, "change_agility"):
        #             caller.add_agility(-self.db.agility_points)
        #     if self.db.stamina_points:
        #         if hasattr(caller, "change_stamina"):
        #             caller.add_stamina(-self.db.stamina_points)
        #     if self.db.smart_points:
        #         if hasattr(caller, "change_smart"):
        #             caller.add_smart(-self.db.smart_points)
        #     if self.db.damage_points:
        #         if hasattr(caller, "change_stamina"):
        #             caller.add_damage(-self.db.damage_points)
        #     if self.db.defend_points:
        #         if hasattr(caller, "change_stamina"):
        #             caller.add_defend(-self.db.defend_points)
        #     if self.db.attack_speed_points:
        #         if hasattr(caller, "change_stamina"):
        #             caller.add_attack_speed(-self.db.attack_speed_points)
        #     if self.db.critical_hit_points:
        #         caller.add_critical_hit(-self.db.critical_hit_points)
        #     if self.db.avoid_points:
        #         if hasattr(caller, "change_stamina"):
        #             caller.add_avoid(-self.db.avoid_points)
        #     if self.db.parry_points:
        #         if hasattr(caller, "change_stamina"):
        #             caller.add_parry(-self.db.parry_points)
        #     if self.db.hit_points:
        #         if hasattr(caller, "change_stamina"):
        #             caller.add_hit(-self.db.hit_points)
        # else:
        #     self.db.is_equiped = True
        #     if self.db.strength_points:
        #         if hasattr(caller, "change_strength"):
        #             caller.add_strength(self.db.strength_points)
        #     if self.db.agility_points:
        #         if hasattr(caller, "change_agility"):
        #             caller.add_agility(self.db.agility_points)
        #     if self.db.stamina_points:
        #         if hasattr(caller, "change_stamina"):
        #             caller.add_stamina(self.db.stamina_points)
        #     if self.db.smart_points:
        #         if hasattr(caller, "change_stamina"):
        #             caller.add_smart(self.db.smart_points)
        #     if self.db.damage_points:
        #         if hasattr(caller, "change_stamina"):
        #             caller.add_damage(self.db.damage_points)
        #     if self.db.defend_points:
        #         if hasattr(caller, "change_stamina"):
        #             caller.add_defend(self.db.defend_points)
        #     if self.db.attack_speed_points:
        #         if hasattr(caller, "change_stamina"):
        #             caller.add_attack_speed(self.db.attack_speed_points)
        #     if self.db.critical_hit_points:
        #         if hasattr(caller, "change_stamina"):
        #             caller.add_critical_hit(self.db.critical_hit_points)
        #     if self.db.avoid_points:
        #         if hasattr(caller, "change_stamina"):
        #             caller.add_avoid(self.db.avoid_points)
        #     if self.db.parry_points:
        #         if hasattr(caller, "change_stamina"):
        #             caller.add_parry(self.db.parry_points)
        #     if self.db.hit_points:
        #         if hasattr(caller, "change_stamina"):
        #             caller.add_hit(self.db.hit_points)

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

    def _set_ticker_combo(self, interval, hook_key, stop=False, caller=None, target=None):
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
            TICKER_HANDLER.add(interval, getattr(self, hook_key), idstring, True, caller, target)


class BaseSkill(Skill):
    DEFINITION = SkillDefinition.BASE_QUANJIAO
    def at_object_creation(self):
        super(BaseSkill, self).at_object_creation()
        self.db.is_equiped = True

class SpecialSkill(Skill):
    DEFINITION = SkillDefinition.BASE_QUANJIAO
    def at_object_creation(self):
        super(SpecialSkill, self).at_object_creation()
        self.db.is_equiped = False