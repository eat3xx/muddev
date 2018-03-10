#coding=utf-8
import commands
from settings.skilldef import SkillDefinition

from typeclasses.item.skill.skill import BaseSkill

class BaseQuanJiao(BaseSkill):
    DEFINITION = SkillDefinition.BASE_QUANJIAO
    def at_object_creation(self):
        super(BaseSkill, self).at_object_creation()
        self.cmdset.add(commands.default_cmdsets.BaseQuanJiaoCmdSet, permanent=True)
        self.db.is_equiped = True

    def set_words(self):
        level = self.db.level
        # self.db.strength_points = int(level/10.00)
        self.db.strength_points = int(level)

    # 使用重击
    def cast(self, caller, target):
        if self.db.is_ready:
            caller.msg("你对敌人使用技能：重击")
            target.db.health -= (self.db.level + caller.db.damage)
            self.db.is_ready = False
            self.start_cooldown()
        else:
            caller.msg("技能还在冷却中...")

class BaseQingGong(BaseSkill):
    DEFINITION = SkillDefinition.BASE_QINGGONG
    def at_object_creation(self):
        super(BaseSkill, self).at_object_creation()
        self.db.is_equiped = True

    def set_words(self):
        level = self.db.level
        self.db.agility_points = int(level)

class BaseNeiGong(BaseSkill):
    DEFINITION = SkillDefinition.BASE_NEIGONG
    def at_object_creation(self):
        super(BaseSkill, self).at_object_creation()
        self.db.is_equiped = True

    def set_words(self):
        level = self.db.level
        self.db.agility_points = int(level)

class BaseZhaoJia(BaseSkill):
    DEFINITION = SkillDefinition.BASE_ZHAOJIA
    def at_object_creation(self):
        super(BaseSkill, self).at_object_creation()
        self.db.is_equiped = True

    def set_words(self):
        level = self.db.level
        self.db.agility_points = int(level)

class BaseJianFa(BaseSkill):
    DEFINITION = SkillDefinition.BASE_JIANFA
    def at_object_creation(self):
        super(BaseSkill, self).at_object_creation()
        self.db.is_equiped = True

    def set_words(self):
        level = self.db.level
        self.db.agility_points = int(level)

class BaseDaoFa(BaseSkill):
    DEFINITION = SkillDefinition.BASE_DAOFA
    def at_object_creation(self):
        super(BaseSkill, self).at_object_creation()
        self.db.is_equiped = True

    def set_words(self):
        level = self.db.level
        self.db.agility_points = int(level)



