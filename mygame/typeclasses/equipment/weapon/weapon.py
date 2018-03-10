#coding=utf-8
from settings.equipmentdef import EquipmentCategory, EquipmentDefinition
from typeclasses.objects import Object
from commands.default_cmdsets import WeaponCmdSet
from typeclasses.equipment.equipment import Equipment
from settings.equipmentdef import WeaponCategory

class Weapon(Equipment):

    DEFINITION = EquipmentDefinition.SWORD_IRONSWORD

    def at_object_creation(self):
        super(Weapon, self).at_object_creation()
        self.cmdset.add(WeaponCmdSet, permanent=True)



