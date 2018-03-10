#coding=utf-8
"""
经验等级对应表
"""

def get_level():
    exp_dict = {}
    exp = 0
    base = 40
    x = 0.01
    for i in range(1,1501):
        base = base * (1 + x)
        exp += base
        exp_dict[i] = int(exp)
    return exp_dict

exp_dict = get_level()
