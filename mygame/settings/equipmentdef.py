#coding=utf-8

#  装备的分类
class EquipmentCategory(object):
    WEAPON = "武器"
    HELMET = "头部"
    NECKLACE = "项链"
    CLOTH = "衣服"
    CLOAK = "披风"
    GLOVE = "护手"
    RING = "戒指"
    ACCESSORY = "饰品"
    BELT = "腰带"
    PANT = "裤子"
    SHOE = "鞋子"
    HIDDEN_WEAPON = "暗器"

# 武器的分类
class WeaponCategory(object):
    SWORD = "剑"
    BLADE = "刀"
    STICK = "棍"

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