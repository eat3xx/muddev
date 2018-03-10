#coding=utf-8
from settings.equipmentdef import EquipmentCategory, WeaponCategory, EquipmentDefinition
from weapon import Weapon
import random

class IronSword(Weapon):
    """
    铁剑，基础剑类武器
    """
    DEFINITION = EquipmentDefinition.SWORD_IRONSWORD

    def at_object_creation(self):
        super(IronSword, self).at_object_creation()

class SharpSword(Weapon):
    """
    利剑，中级剑类武器
    """
    DEFINITION = EquipmentDefinition.SWORD_SHARPSWORD

    def at_object_creation(self):
        super(SharpSword, self).at_object_creation()

class ChampionSword(Weapon):
    """
    冠军剑，高级剑类武器
    """
    DEFINITION = EquipmentDefinition.SWORD_CHAMPIONSWORD

    def at_object_creation(self):
        super(ChampionSword, self).at_object_creation()

# if __name__ == '__main__':
#     a = Longsword()
#     print 3
#     print type(a)
#     print 1
#     print a.__class__.__name__
