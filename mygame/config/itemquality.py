#coding=utf-8
"""
此文件定义武器的品质
武器的品质类型,分为
  普通：plain, 颜色：white
  精良：polish, 颜色：green
  稀有：rare, 颜色：blue
  精英：elite, 颜色：purple：
  史诗：epic, 颜色：orange
  传说：legendary, 颜色：darkgolden (暂时不提供)
"""
import random

# 装备品质列表
qualities = ["plain", "polish", "rare", "elite", "epic"]

# 人物属性加成词缀，每个词缀出现一次代表：力量加一，敏捷加一，耐力加一
attr_words = ["strength", "agility","stamina"]

# 武器本身加成词缀,每个词缀出现一次代表：伤害加成百分之一，攻速加成百分之一，暴击率加百分之一
weapon_damage_words = ["damage", "speed", "criticalhit"]

# 武器效果词缀，
weapon_effect_words = ["bleeding", "penetration"]

class Quality():
    # def __init__(self):
    #     # self.id = "plain"
    #     # self.color = "white"
    #     # self.point = 0

    def getName(self):
        return self.name

    def getId(self):
        return self.id

    def getColor(self):
        return self.color

    def getWords(self):
        return self.words

class Plain(Quality):
    def __init__(self):
        self.id = 1
        self.name = "plain"
        self.color = "white"
        self.words = []

class Polish(Quality):
    def __init__(self):
        self.id = 2
        self.name = "polish"
        self.color = "green"
        self.words = self.createwords()

    def createwords(self):
        words = []
        # 绿色装备，抽取两条属性词缀
        for i in range(0, 5):
            words.append(random.choice(attr_words))
        return words

class Rare(Quality):
    def __init__(self):
        self.id = 3
        self.name = "rare"
        self.color = "blue"
        self.words = self.createwords()

    def createwords(self):
        words = []
        # 蓝色装备，抽取10条属性词缀
        for i in range(0, 15):
            words.append(random.choice(attr_words))
        return words

class Elite(Quality):
    def __init__(self):
        self.id = 4
        self.name = "elite"
        self.color = "purple"
        self.words = self.createwords()

    def createwords(self):
        words = []
        # 紫色装备，抽取20条属性词缀
        for i in range(0, 25):
            words.append(random.choice(attr_words))
        # 紫色装备，抽取10条武器词缀
        for i in range(0, 25):
            words.append(random.choice(weapon_damage_words))
        return words

class Epic(Quality):
    def __init__(self):
        self.id = 5
        self.name = "epic"
        self.color = "orange"
        self.words = self.createwords()

    def createwords(self):
        words = []
        # 橙色装备，抽取50条属性词缀
        for i in range(0, 50):
            words.append(random.choice(attr_words))
        # 橙色装备，抽取50条武器词缀
        for i in range(0, 50):
            words.append(random.choice(weapon_damage_words))
        return words


