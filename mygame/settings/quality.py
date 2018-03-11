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

from settings.charspec import AttrWord
from settings.general import Color


class QualityName(object):
    PLAIN = "普通"
    POLISH = "高级"
    RARE = "稀有"
    ELITE = "精英"
    EPIC = "史诗"

qualities = ["plain", "polish", "rare", "elite", "epic"]

class Quality():
    ID = 0
    NAME = QualityName.PLAIN
    COLOR = Color.WHITE
    WORDS= None

    def __init__(self):
        self.id = self.ID
        self.name = self.NAME
        self.color = self.COLOR
        self.words = self.WORDS

    def getName(self):
        return self.name

    def getId(self):
        return self.id

    def getColor(self):
        return self.color

    def getWords(self):
        return self.words


class PlainWeapon(Quality):
    ID = 1
    NAME = QualityName.PLAIN
    COLOR = Color.WHITE
    WORDS = {AttrWord.DAMAGE: 0,
             AttrWord.AGILITY: 0,
             AttrWord.ATTACK_SPEED: 0,
             AttrWord.CRITIAL_HIT: 0,
             AttrWord.HIT: 0,
             AttrWord.PARRY: 0,
             AttrWord.STAMINA: 0,
             AttrWord.STRENGTH: 0}


class PolishWeapon(Quality):
    ID = 2
    NAME = QualityName.POLISH
    COLOR = Color.GREEN
    WORDS = {AttrWord.DAMAGE: 20,
             AttrWord.AGILITY: 10,
             AttrWord.ATTACK_SPEED: 0,
             AttrWord.CRITIAL_HIT: 0,
             AttrWord.HIT: 20,
             AttrWord.PARRY: 20,
             AttrWord.STAMINA: 5,
             AttrWord.STRENGTH: 20}

class RareWeapon(Quality):
    ID = 3
    NAME = QualityName.RARE
    COLOR = Color.BLUE
    WORDS = {AttrWord.DAMAGE: 30,
             AttrWord.AGILITY: 20,
             AttrWord.ATTACK_SPEED: 2,
             AttrWord.CRITIAL_HIT: 2,
             AttrWord.HIT: 30,
             AttrWord.PARRY: 30,
             AttrWord.STAMINA: 15,
             AttrWord.STRENGTH: 30}

class EliteWeapon(Quality):
    ID = 4
    NAME = QualityName.ELITE
    COLOR = Color.PURPLE
    WORDS = {AttrWord.DAMAGE: 40,
             AttrWord.AGILITY: 30,
             AttrWord.ATTACK_SPEED: 5,
             AttrWord.CRITIAL_HIT: 5,
             AttrWord.HIT: 40,
             AttrWord.PARRY: 40,
             AttrWord.STAMINA: 25,
             AttrWord.STRENGTH: 40}

class EpicWeapon(Quality):
    ID = 5
    NAME = QualityName.EPIC
    COLOR = Color.ORANGE
    WORDS = {AttrWord.DAMAGE: 50,
             AttrWord.AGILITY: 40,
             AttrWord.ATTACK_SPEED: 10,
             AttrWord.CRITIAL_HIT: 10,
             AttrWord.HIT: 50,
             AttrWord.PARRY: 50,
             AttrWord.STAMINA: 35,
             AttrWord.STRENGTH: 50}


