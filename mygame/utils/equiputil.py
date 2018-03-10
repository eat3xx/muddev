#coding=utf-8

def at_equip_skill(obj, caller, reverse=False):
    at_equip_equipment(obj, caller, reverse=reverse)

def at_equip_equipment(obj, caller, reverse=False):
    """
    装备上物品，并把装备上的属性添加到人物身上。
    当 reverse=True 的时候把装备上的属性从人物身上取消。
    :param caller: 人物，命令调用者
    :param self: 装备物品
    :param reverse: 开关，控制装备或者脱下
    :return: 无
    """
    if reverse:
        obj.db.is_equiped = False
        if obj.db.strength_points:
            if hasattr(caller, "add_strength"):
                caller.add_strength(-obj.db.strength_points)
        if obj.db.agility_points:
            if hasattr(caller, "add_agility"):
                caller.add_agility(-obj.db.agility_points)
        if obj.db.stamina_points:
            if hasattr(caller, "add_stamina"):
                caller.add_stamina(-obj.db.stamina_points)
        if obj.db.smart_points:
            if hasattr(caller, "add_smart"):
                caller.add_smart(-obj.db.smart_points)
        if obj.db.damage_points:
            if hasattr(caller, "add_damage"):
                caller.add_damage(-obj.db.damage_points)
        if obj.db.defend_points:
            if hasattr(caller, "add_defend"):
                caller.add_defend(-obj.db.defend_points)
        if obj.db.attack_speed_points:
            if hasattr(caller, "add_attack_speed"):
                caller.add_attack_speed(-obj.db.attack_speed_points)
        if obj.db.critical_hit_points:
            if hasattr(caller, "add_critical_hit"):
                caller.add_critical_hit(-obj.db.critical_hit_points)
        if obj.db.avoid_points:
            if hasattr(caller, "add_avoid"):
                caller.add_avoid(-obj.db.avoid_points)
        if obj.db.parry_points:
            if hasattr(caller, "add_parry"):
                caller.add_parry(-obj.db.parry_points)
        if obj.db.hit_points:
            if hasattr(caller, "add_hit"):
                caller.add_hit(-obj.db.hit_points)
    else:
        obj.db.is_equiped = True
        if obj.db.strength_points:
            if hasattr(caller, "add_strength"):
                caller.add_strength(obj.db.strength_points)
        if obj.db.agility_points:
            if hasattr(caller, "add_agility"):
                caller.add_agility(obj.db.agility_points)
        if obj.db.stamina_points:
            if hasattr(caller, "add_stamina"):
                caller.add_stamina(obj.db.stamina_points)
        if obj.db.smart_points:
            if hasattr(caller, "add_smart"):
                caller.add_smart(obj.db.smart_points)
        if obj.db.damage_points:
            if hasattr(caller, "add_damage"):
                caller.add_damage(obj.db.damage_points)
        if obj.db.defend_points:
            if hasattr(caller, "add_defend"):
                caller.add_defend(obj.db.defend_points)
        if obj.db.attack_speed_points:
            if hasattr(caller, "add_attack_speed"):
                caller.add_attack_speed(obj.db.attack_speed_points)
        if obj.db.critical_hit_points:
            if hasattr(caller, "add_critical_hit"):
                caller.add_critical_hit(obj.db.critical_hit_points)
        if obj.db.avoid_points:
            if hasattr(caller, "add_avoid"):
                caller.add_avoid(obj.db.avoid_points)
        if obj.db.parry_points:
            if hasattr(caller, "add_parry"):
                caller.add_parry(obj.db.parry_points)
        if obj.db.hit_points:
            if hasattr(caller, "add_hit"):
                caller.add_hit(obj.db.hit_points)