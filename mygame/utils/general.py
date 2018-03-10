#coding=utf-8

import random
from evennia.utils import utils
from typeclasses.equipment.equipment import Equipment
from typeclasses.item.skill.baseskills import BaseSkill
from typeclasses.item.skill.huashan.skills import SpecialSkill
from typeclasses.item.skill.skill import Skill


def get_all_equipments(caller):
    """
    获取人物身上所有装备
    :param caller: 当前角色，命令调用者
    :return: 空，或者 装备
    """
    items = caller.contents
    equiped_items = []
    for item in items:
        if isinstance(item, Equipment):
            equiped_items.append(item)
    return equiped_items

def get_equiped_equipments(caller):
    """
    获取人物身上所有已经装备的物品
    :param caller: 当前角色，命令调用者
    :return: 空，或者 装备
    """
    items = get_all_equipments(caller)
    equiped_items = []
    for item in items:
        if item.db.is_equiped == True:
            equiped_items.append(item)
    return equiped_items

def get_equiped_equipment_by_type(caller, type):
    """
    获取人物当前指定位置的装备，比如得到人物当前头部装备
    :param caller: 当前角色，命令调用者
    :param type: 人体部位，为EquipmentCategory中的常量
    :return: 空，或者 装备
    """
    items = get_equiped_equipments(caller)
    for item in items:
        if type == item.EQUIPMENT_TYPE:
            return item
    return None

def get_all_skills(caller):
    """
    获取人物身上所有学会的技能
    :param caller: 当前角色，命令调用者
    :return: 空，或者 技能
    """
    items = caller.contents
    equiped_items = []
    for item in items:
        if isinstance(item, Skill):
            equiped_items.append(item)
    return equiped_items

def get_all_base_skills(caller):
    """
    获取人物身上所有学会的基础技能
    :param caller: 当前角色，命令调用者
    :return: 空，或者 技能
    """
    items = get_all_skills(caller)
    equiped_items = []
    for item in items:
        if isinstance(item, BaseSkill):
            equiped_items.append(item)
    return equiped_items

def get_base_skill_by_type(caller, type):
    """
    获取人物身上某个位置的基础技能，比如获取人物拳脚部位的技能
    :param caller: 当前角色，命令调用者
    :return: 空，或者 技能
    """
    items = get_all_base_skills(caller)
    for item in items:
        if type == item.db.type:
            return item
    return None

def get_all_special_skills(caller):
    """
    获取人物身上所有学会的特殊技能
    :param caller: 当前角色，命令调用者
    :return: 空，或者 技能
    """
    items = get_all_skills(caller)
    equiped_items = []
    for item in items:
        if isinstance(item, SpecialSkill):
            equiped_items.append(item)
    return equiped_items

def get_equiped_special_skills(caller):
    """
    获取人物身上所有已装备的特殊技能
    :param caller: 当前角色，命令调用者
    :return: 空，或者 技能
    """
    items = get_all_special_skills(caller)
    equiped_items = []
    for item in items:
        if item.db.is_equiped:
            equiped_items.append(item)
    return equiped_items

def get_equiped_special_skill_by_type(caller, type):
    """
    获取人物身上某个位置的特殊技能，比如获取人物拳脚部位的特殊技能
    :param caller: 当前角色，命令调用者
    :return: 空，或者 技能
    """
    items = get_equiped_special_skills(caller)
    for item in items:
        if type == item.db.type:
            return item
    return None

def determine_quality(rate):
    """
    # 决定物品掉落的品质。
    :param rate: 寻宝率
    :return: 品质
    """
    # 产生一个0-1之间的随机数
    random_number = random.random()
    # 如果几率为20%, 则有20%几率为绿色，10%几率为蓝色，4%几率为紫色，1%几率为橙色
    if random_number < rate:
        quality = quality.EpicWeapon()
    else:
        if random_number < rate / 5:
            quality = quality.EliteWeapon()
        else:
            if random_number < rate / 2:
                quality = quality.RareWeapon()
            else:
                if random_number < rate:
                    quality = quality.PolishWeapon()
                else:
                    quality = quality.PlainWeapon()
    return quality

def determine_one_hit(be_attacked, attacker):
    """
    决定是否被对方击中，以及击中后的伤害计算
    :param self:
    :param attacker:
    :return:
    """
    # 敌方伤害值
    damage_taken = attacker.db.damage
    # 是否命中标志
    binggo = False
    rate = 0.00
    # 判定是否招架成功, 命中几率为命中除以两倍的招架
    rate = attacker.db.hit / float(be_attacked.db.parry) / 2.00
    if random.random() < rate:
        # 判定是否躲闪成功，命中几率为命中除以两倍的躲闪
        rate = attacker.db.hit / float(be_attacked.db.avoid) / 2.00
        if random.random() < rate:
            binggo = True
        else:
            attacker.msg("你的攻击被 %s 躲闪" % be_attacked.key)
            be_attacked.msg("你躲闪了 %s 的攻击" % (attacker.key))
    else:
        attacker.msg("你的攻击被 %s 格挡" % be_attacked.key)
        be_attacked.msg("你格挡了 %s 的攻击" % (attacker.key))

    # 如果命中，则减去自身防御值后为最终伤害
    is_critical = False
    if binggo:
        # 判断敌方是否暴击，如暴击则伤害加倍
        if random.random() < attacker.db.critical_hit:
            damage_taken *= 2
            is_critical = True
        # 减去自身防御
        damage_taken -= be_attacked.db.defend
        if damage_taken > 0:
            be_attacked.db.health -= damage_taken
            if is_critical:
                attacker.msg("你对 %s 造成了 %s 点暴击伤害" % (be_attacked.key, damage_taken))
                be_attacked.msg("%s 对你造成了 %s 点暴击伤害" % (attacker.key, damage_taken))
            else:
                attacker.msg("你对 %s 造成了 %s 点伤害" % (be_attacked.key, damage_taken))
                be_attacked.msg("%s 对你造成了 %s 点伤害" % (attacker.key, damage_taken))
        else:
            attacker.msg("你的攻击未能对 %s 造成任何伤害" % be_attacked.key)
            be_attacked.msg("%s 的攻击未对你造成任何伤害" % attacker.key)

    if be_attacked.db.health <= 0:
        be_attacked.location.msg_contents("%s 重重倒下了" % be_attacked.key, exclude=be_attacked)
        be_attacked.msg("你已经死亡")
        attacker.msg("%s 已经死亡" % be_attacked.key)
        be_attacked.set_dead()
    else:
        if not be_attacked.ndb.is_attacking:
            be_attacked.db.current_enemy = attacker
            attacker.msg("%s 开始对你发起攻击" % be_attacked.key)
            be_attacked.start_attacking()

def holds(caller, obj):
    contents = caller.contents
    for item in contents:
        if obj == item.db.name:
            return True
    return False

# def holds(caller, obj):
#     print "1"
#     try:
#         print "2"
#         contents = caller.contents
#     except AttributeError:
#         try:
#             print "3"
#             contents = caller.contents
#         except AttributeError:
#             return False
#
#     def check_holds(objid):
#         # helper function. Compares both dbrefs and keys/aliases.
#         objid = str(objid)
#         dbref = utils.dbref(objid, reqhash=False)
#         if dbref and any((True for obj in contents if obj.dbid == dbref)):
#             return True
#         objid = objid.lower()
#         return any((True for obj in contents
#                     if obj.key.lower() == objid or objid in [al.lower() for al in obj.aliases.all()]))
#
#     print "4"
#     try:
#         if check_holds(obj.dbid):
#             print "5"
#             return True
#     except Exception:
#         # we need to catch any trouble here
#         pass
#     print "6"
#     return hasattr(caller, "obj") and check_holds(caller.obj.dbid)