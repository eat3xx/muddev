#coding=utf-8
from settings.general import Color


class SkillCategory(object):
    QUANJIAO = "拳脚"
    QINGGONG = "轻功"
    NEIGONG = "内功"
    ZHAOJIA = "招架"
    JIANFA = "剑法"
    DAOFA = "刀法"

class SkillDesc(object):
    CHU_XUE_ZHA_LIAN = "初学乍练"
    CHU_TONG_PI_MAO = "初通皮毛"
    BAN_SHENG_BU_SHU = "半生不熟"
    MA_MA_HU_HU = "马马虎虎"
    PING_DAN_WU_QI = "平淡无奇"
    JIA_QING_JIU_SHU = "驾轻就熟"
    CHU_RU_JIA_JING = "初入佳境"
    XIN_LING_SHEN_HUI = "心领神会"
    CHAO_QUN_JUE_LUN = "超群绝伦"
    CHAO_FNA_RU_SHENG = "超凡入圣"

class SkillDefinition(object):

    BASE_QINGGONG = {
        "name":"基本轻功",
        "category": SkillCategory.QINGGONG,
        "classpath":"typeclasses.item.skill.baseskills.BaseQingGong",
        "color": Color.WHITE,
        "cooldown": 10
    }

    BASE_NEIGONG = {
        "name":"基本内功",
        "category": SkillCategory.NEIGONG,
        "classpath":"typeclasses.item.skill.baseskills.BaseNeiGong",
        "color": Color.WHITE,
        "cooldown": 10
    }

    BASE_QUANJIAO = {
        "name":"基本拳脚",
        "category": SkillCategory.QUANJIAO,
        "classpath":"typeclasses.item.skill.baseskills.BaseQuanJiao",
        "color": Color.WHITE,
        "cooldown": 10
    }

    BASE_ZHAOJIA = {
        "name": "基本招架",
        "category": SkillCategory.ZHAOJIA,
        "classpath": "typeclasses.item.skill.baseskills.BaseZhaoJia",
        "color": Color.WHITE,
        "cooldown": 10
    }

    BASE_JIANFA = {
        "name": "基本剑法",
        "category": SkillCategory.JIANFA,
        "classpath": "typeclasses.item.skill.baseskills.BaseJianFa",
        "color": Color.WHITE,
        "cooldown": 10
    }

    BASE_DAOFA = {
        "name": "基本刀法",
        "category": SkillCategory.DAOFA,
        "classpath": "typeclasses.item.skill.baseskills.BaseDaoFa",
        "color": Color.WHITE,
        "cooldown": 10}

    SPEC_TAIZUCHANGQUAN = {
        "name": "太祖长拳",
        "category": SkillCategory.QUANJIAO,
        "classpath": "typeclasses.item.skill.freeman.skills.TaiZuChangQuan",
        "color": Color.GREEN,
        "cooldown": 10
    }

    SPEC_HUASHANQUANFA = {
        "name": "华山拳法",
        "category": SkillCategory.QUANJIAO,
        "classpath": "typeclasses.item.skill.huashan.skills.HuaShanQuanFa",
        "color": Color.GREEN,
        "cooldown": 10
    }

    lists = (BASE_QUANJIAO, BASE_QINGGONG, BASE_NEIGONG, BASE_ZHAOJIA, BASE_DAOFA, BASE_JIANFA, SPEC_HUASHANQUANFA, SPEC_TAIZUCHANGQUAN)

    @staticmethod
    def get_skill_by_name(name, list=lists):
        for item in list:
            if name == item.get("name").strip():
                return item
        return None