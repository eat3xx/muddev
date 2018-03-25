#coding=utf-8
import commands
from settings.charspec import AttrWord

from settings.equipmentdef import EquipmentDefinition
from typeclasses.objects import Object
from utils.equiputil import at_equip_equipment

class Equipment(Object):

    DEFINITION = EquipmentDefinition.SWORD_IRONSWORD

    def at_object_creation(self):
        super(Equipment, self).at_object_creation()
        self.cmdset.add(commands.default_cmdsets.EquipmentCmdSet, permanent=True)

        # 武器类型
        self.db.type = self.DEFINITION.get("category")
        self.db.catetory = self.DEFINITION.get("subcategory")
        self.db.name = self.DEFINITION.get("name")
        self.db.base_damage = self.DEFINITION.get("basedamage")

        # 武器颜色
        self.db.color = None
        self.db.quality = None

        # 是否被装备上
        self.db.is_equiped = False

        # 武器对人物属性点的加点
        self.db.strength_points = 0
        self.db.agility_points = 0
        self.db.stamina_points = 0
        self.db.smart_points = 0

        # 武器对人物战斗属性的加成
        self.db.damage_points = 0
        self.db.defend_points = 0
        self.db.attack_speed_points = 0
        self.db.critical_hit_points = 0
        self.db.avoid_points = 0
        self.db.parry_points = 0
        self.db.hit_points = 0

    def return_appearance(self, looker):
        """
        The return from this method is what
        looker sees when looking at this object.
        """
        # text = super(Equipment, self).return_appearance(looker)
        cscore = "%s%s|n  %s%s" % (self.db.color, self.db.name, self.db.quality, self.db.type) + "\n"  + \
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
        # if "\n" in text:
        #     # text is multi-line, add score after first line
        #     first_line, rest = text.split("\n", 1)
        #     text = first_line + cscore + "\n" + rest
        # else:
        #     # text is only one line; add score to end
        #     text += cscore
        return cscore

    def set_quality(self, quality):
        self.db.color = quality.getColor()
        self.db.quality = quality.getName()
        words = quality.getWords()

        # 以下属性在装备时会添加到人物属性
        if words.has_key(AttrWord.STRENGTH):
            self.db.strength_points = words.get(AttrWord.STRENGTH)
        if words.has_key(AttrWord.AGILITY):
            self.db.agility_points = words.get(AttrWord.AGILITY)
        if words.has_key(AttrWord.STAMINA):
            self.db.stamina_points = words.get(AttrWord.STAMINA)
        if words.has_key(AttrWord.SMART):
            self.db.smart_points = words.get(AttrWord.SMART)
        if words.has_key(AttrWord.DAMAGE):
            self.db.damage_points = words.get(AttrWord.DAMAGE)
            if self.db.base_damage:
                self.db.damage_points += self.db.base_damage
        if words.has_key(AttrWord.DEFEND):
            self.db.defend_points = words.get(AttrWord.DEFEND)
        if words.has_key(AttrWord.ATTACK_SPEED):
            self.db.attack_speed_points = words.get(AttrWord.ATTACK_SPEED)
        if words.has_key(AttrWord.CRITIAL_HIT):
            self.db.critical_hit_points = words.get(AttrWord.CRITIAL_HIT)
        if words.has_key(AttrWord.PARRY):
            self.db.parry_points = words.get(AttrWord.PARRY)
        if words.has_key(AttrWord.AVOID):
            self.db.avoid_points = words.get(AttrWord.AVOID)
        if words.has_key(AttrWord.HIT):
            self.db.hit_points = words.get(AttrWord.HIT)

    def at_equip(self, caller, reverse=False):
        """
        装备上物品，并把装备上的属性添加到人物身上。
        当 reverse=True 的时候把装备上的属性从人物身上取消。
        :param caller: 人物，命令调用者
        :param self: 装备物品
        :param reverse: 开关，控制装备或者脱下
        :return: 无
        """

        at_equip_equipment(self, caller, reverse=reverse)
        # if reverse:
        #     self.db.is_equiped = False
        #     if self.db.strength_points:
        #         caller.add_strength(-self.db.strength_points)
        #     if self.db.agility_points:
        #         caller.add_agility(-self.db.agility_points)
        #     if self.db.stamina_points:
        #         caller.add_stamina(-self.db.stamina_points)
        #     if self.db.smart_points:
        #         caller.add_smart(-self.db.smart_points)
        #     if self.db.damage_points:
        #         caller.add_damage(-self.db.damage_points)
        #     if self.db.defend_points:
        #         caller.add_defend(-self.db.defend_points)
        #     if self.db.attack_speed_points:
        #         caller.add_attack_speed(-self.db.attack_speed_points)
        #     if self.db.critical_hit_points:
        #         caller.add_critical_hit(-self.db.critical_hit_points)
        #     if self.db.avoid_points:
        #         caller.add_avoid(-self.db.avoid_points)
        #     if self.db.parry_points:
        #         caller.add_parry(-self.db.parry_points)
        #     if self.db.hit_points:
        #         caller.add_hit(-self.db.hit_points)
        # else:
        #     self.db.is_equiped = True
        #     if self.db.strength_points:
        #         caller.add_strength(self.db.strength_points)
        #     if self.db.agility_points:
        #         caller.add_agility(self.db.agility_points)
        #     if self.db.stamina_points:
        #         caller.add_stamina(self.db.stamina_points)
        #     if self.db.smart_points:
        #         caller.add_smart(self.db.smart_points)
        #     if self.db.damage_points:
        #         caller.add_damage(self.db.damage_points)
        #     if self.db.defend_points:
        #         caller.add_defend(self.db.defend_points)
        #     if self.db.attack_speed_points:
        #         caller.add_attack_speed(self.db.attack_speed_points)
        #     if self.db.critical_hit_points:
        #         caller.add_critical_hit(self.db.critical_hit_points)
        #     if self.db.avoid_points:
        #         caller.add_avoid(self.db.avoid_points)
        #     if self.db.parry_points:
        #         caller.add_parry(self.db.parry_points)
        #     if self.db.hit_points:
        #         caller.add_hit(self.db.hit_points)

