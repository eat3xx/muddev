#coding=utf-8

from weapon import Weapon
import random

class Longsword(Weapon):
    """
    长剑，基础剑类武器
    """
    # 武器基本类型
    WEAPON_TYPE = "sword"
    # 基础伤害
    BASE_DAMAGE = 10
    # 基础攻击速度
    BASE_ATTACK_SPEED = 5
    # 基础暴击几率
    BASE_CRITICAL_HIT = 0

    def at_object_creation(self):
        super(Longsword, self).at_object_creation()

class Sharpsword(Weapon):
    """
    利剑，中级剑类武器
    """
    # 武器基本类型
    WEAPON_TYPE = "sword"
    # 基础伤害
    BASE_DAMAGE = 20
    # 基础攻击速度
    BASE_ATTACK_SPEED = 5
    # 基础暴击几率
    BASE_CRITICAL_HIT = 3

    def at_object_creation(self):
        super(Sharpsword, self).at_object_creation()

class Championsword(Weapon):
    """
    冠军剑，高级剑类武器
    """
    # 武器基本类型
    WEAPON_TYPE = "sword"
    # 基础伤害
    BASE_DAMAGE = 30
    # 基础攻击速度
    BASE_ATTACK_SPEED = 5
    # 基础暴击几率
    BASE_CRITICAL_HIT = 6

    def at_object_creation(self):
        super(Championsword, self).at_object_creation()