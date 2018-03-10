#coding=utf-8

from settings.skilldef import SkillDefinition
from typeclasses.item.skill.skill import SpecialSkill


class HuaShanQuanFa(SpecialSkill):
    DEFINITION = SkillDefinition.SPEC_HUASHANQUANFA
    def at_object_creation(self):
        super(HuaShanQuanFa, self).at_object_creation()
        self.db.is_equiped = False

    def set_words(self):
        level = self.db.level
        if level < 100:
            # 小于100级时，每级加2点攻击
            self.db.damage_points = level*2
        else:
            # 大于100级是，每级加1点攻击
            self.db.damage_points = 200 + (level-100)