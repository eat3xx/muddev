#coding=utf-8
from settings.equipmentdef import EquipmentCategory, WeaponCategory, EquipmentDefinition
from weapon import Weapon
import random

class SteelBlade(Weapon):
    """
    钢刀，基础刀类武器
    """
    DEFINITION = EquipmentDefinition.BLADE_STEELBLADE

    def at_object_creation(self):
        super(SteelBlade, self).at_object_creation()

class SharpBlade(Weapon):
    """
    利刃，中级刀类武器
    """
    DEFINITION = EquipmentDefinition.BLADE_SHARPBLADE

    def at_object_creation(self):
        super(SharpBlade, self).at_object_creation()

class ChampionBlade(Weapon):
    """
    冠军之刃，高级刀类武器
    """
    DEFINITION = EquipmentDefinition.BLADE_CHAMPIONBLADE

    def at_object_creation(self):
        super(ChampionBlade, self).at_object_creation()

# if __name__ == '__main__':
#     a = Longsword()
#     print 3
#     print type(a)
#     print 1
#     print a.__class__.__name__
