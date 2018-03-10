#coding=utf-8
from settings import rank
from settings.equipmentdef import EquipmentDefinition
from settings.general import Color, Gender
from settings.skilldef import SkillDefinition


class HuaShanMaster(object):

    GAOGENMING = {
        "classpath": "typeclasses.npc.huashan.GaoGenMing",
        "gender" : Gender.MALE,
        "name" : "高根明",
        "rank" : rank.crusader,
        "damage": 10,
        "defend": 10,
        "attack_speed": 4,
        "critical_hit": 0.01,
        "parry": 10,
        "avoid": 10,
        "hit": 10,
        "full_health": 1000,
        "full_energy": 1000,
        "is_dead": False,
        "immortal": False,
        "magic_found" : 0.99,
        "available_drop_items" : [EquipmentDefinition.SWORD_IRONSWORD, EquipmentDefinition.SWORD_SHARPSWORD, EquipmentDefinition.SWORD_CHAMPIONSWORD],
        "skills" : [SkillDefinition.BASE_QUANJIAO, SkillDefinition.BASE_QINGGONG],
        "skill_level" : 300
    }

    #
    # __all__ = (HUASHAN_GAOGENMING,)
    #
    # def get_skill_by_name(self, name):
    #     for item in self.__all__:
    #         if name == item.get("name"):
    #             return item
    #     return None