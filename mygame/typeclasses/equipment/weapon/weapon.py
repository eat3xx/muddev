#coding=utf-8

from typeclasses.objects import Object
from commands.default_cmdsets import WeaponCmdSet
from typeclasses.equipment.equipment import Equipment

import random

sword = "sword"
sharpsword = "sharpsword"
championsword = "championsword"

class Weapon(Equipment):

    # 武器基本类型
    WEAPON_TYPE = None
    # 基础伤害 (该值被具体子类重置)
    BASE_DAMAGE = 5
    # 基础攻击速度为 3 秒 一次 (该值被具体子类重置)
    BASE_ATTACK_SPEED = 3
    # 基础暴击几率为 0 (该值被具体子类重置)
    BASE_CRITICAL_HIT = 0

    def at_object_creation(self):
        super(Weapon, self).at_object_creation()
        self.cmdset.add(WeaponCmdSet, permanent=True)
        # 武器类型
        self.db.type = self.WEAPON_TYPE
        # 武器伤害
        self.db.damage =  self.BASE_DAMAGE
        # 武器速度
        self.db.speed = self.BASE_ATTACK_SPEED
        # 武器暴击率
        self.db.critical_hit = self.BASE_CRITICAL_HIT
        # 武器颜色
        self.db.color = None
        # 武器对人物属性的加点
        self.db.strength_points = 0
        self.db.agility_points = 0
        self.db.stamina_points = 0

        self.db.damage_points = 0
        self.db.speed_points = 0
        self.db.critical_hit_points = 0

    def return_appearance(self, looker):
        """
        The return from this method is what
        looker sees when looking at this object.
        """
        text = super(Weapon, self).return_appearance(looker)
        cscore = "类型: %s (%s)" % (self.db.type, self.db.color) + "\n"  + \
                 "伤害: %s" % self.db.damage + "\n" + \
                 "攻击速度: %s" % self.db.speed + "\n" + \
                 "附加属性:" + "\n" + \
                 "  力量 + %s" % self.db.strength_points + "\n" + \
                 "  敏捷 + %s" % self.db.agility_points + "\n" + \
                 "  耐力 + %s" % self.db.stamina_points + "\n" + \
                 "  伤害提高百分之%s" % self.db.damage_points + "\n" + \
                 "  攻速提高百分之%s" % self.db.speed_points + "\n" + \
                 "  暴击几率提高百分之%s" % self.db.critical_points
        if "\n" in text:
            # text is multi-line, add score after first line
            first_line, rest = text.split("\n", 1)
            text = first_line + cscore + "\n" + rest
        else:
            # text is only one line; add score to end
            text += cscore
        return text

    def set_quality(self, quality):
        self.db.color = quality.getColor()
        self.db.words = quality.getWords()

        # 以下属性在装备时会添加到人物属性
        self.db.strength_points = self.db.words.count("strength")
        self.db.agility_points = self.db.words.count("agility")
        self.db.stamina_points = self.db.words.count("stamina")

        # 以下属性直接改变武器自身属性
        self.db.damage_points = self.db.words.count("damage")
        self.db.speed_points = self.db.words.count("speed")
        self.db.critical_points = self.db.words.count("criticalhit")

        self.db.damage *= (1 + self.db.damage_points/100.00)
        self.db.damage = round(self.db.damage)
        self.db.speed *= (1 - self.db.speed_points / 100.00)
        self.db.critical_hit += (self.db.critical_points / 100.00)



