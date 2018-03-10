#coding=utf-8
import commands
from settings.skilldef import SkillDefinition
from typeclasses.item.skill.skill import SpecialSkill
from utils.general import determine_one_hit


class TaiZuChangQuan(SpecialSkill):
    """
    太祖长拳。8秒内每秒出拳一次，每次造成普通攻击伤害，期间自身躲闪为0
    """
    DEFINITION = SkillDefinition.SPEC_TAIZUCHANGQUAN
    def at_object_creation(self):
        super(TaiZuChangQuan, self).at_object_creation()
        self.cmdset.add(commands.default_cmdsets.TaiZuChangQuanCmdSet, permanent=True)
        self.db.is_equiped = False

    def set_words(self):
        level = self.db.level
        self.db.damage_points = level + 20

    def cast(self, caller, target):
        if self.db.is_ready:
            caller.msg("你对%s使用技能：太祖八式" % target.name)
            self.db.is_ready = False
            self.start_taizubashi(caller, target)
        else:
            caller.msg("技能还在冷却中...")

    count = 1
    def do_taizubashi(self, caller, target):
        caller.msg("第%s拳" % self.count)
        determine_one_hit(target, caller)
        self.count += 1
        if target.db.health < 0 or self.count > 8 :
            self.count = 1
            self.start_cooldown()

    def start_taizubashi(self, caller, target):
        self._set_ticker_combo(1, "do_taizubashi", caller=caller, target=target)
