#coding=utf-8

#  装备的分类
class EquipmentCategory(object):
    HELMET = "helmet"
    NECKLACE = "necklace"
    CLOTH = "cloth"
    CLOAK = "cloak"
    GLOVE = "glove"
    RING = "ring"
    ACCESSORY = "accessory"
    BELT = "belt"
    PANT = "pant"
    SHOE = "shoe"
    WEAPON = "weapon"
    HIDDEN_WEAPON = "hidden_weapon"

# 武器的分类
class WeaponCategory(object):
    SWORD = "sword"
    BLADE = "blade"
    STICK = "stick"

class EquipmentDefinition(object):

    SWORD_IRONSWORD = {
        "name": "铁剑",
        "category": EquipmentCategory.WEAPON,
        "subcategory": WeaponCategory.SWORD,
        "classpath": "typeclasses.equipment.weapon.sword.IronSword",
        "basedamage": 10
    }

    SWORD_SHARPSWORD = {
        "name": "利剑",
        "category": EquipmentCategory.WEAPON,
        "subcategory": WeaponCategory.SWORD,
        "classpath": "typeclasses.equipment.weapon.sword.SharpSword",
        "basedamage": 20
    }

    SWORD_CHAMPIONSWORD = {
        "name": "冠军剑",
        "category": EquipmentCategory.WEAPON,
        "subcategory": WeaponCategory.SWORD,
        "classpath": "typeclasses.equipment.weapon.sword.ChampionSword",
        "basedamage": 30
    }

    BLADE_STEELBLADE = {
        "name": "钢刀",
        "category": EquipmentCategory.WEAPON,
        "subcategory": WeaponCategory.BLADE,
        "classpath": "typeclasses.equipment.weapon.sword.SteelBlade",
        "basedamage": 10
    }

    BLADE_SHARPBLADE = {
        "name": "利刃",
        "category": EquipmentCategory.WEAPON,
        "subcategory": WeaponCategory.BLADE,
        "classpath": "typeclasses.equipment.weapon.sword.SharpBlade",
        "basedamage": 20
    }

    BLADE_CHAMPIONBLADE = {
        "name": "冠军之刃",
        "category": EquipmentCategory.WEAPON,
        "subcategory": WeaponCategory.BLADE,
        "classpath": "typeclasses.equipment.weapon.sword.ChampionBlade",
        "basedamage": 30
    }