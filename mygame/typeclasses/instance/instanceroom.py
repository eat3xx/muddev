#coding=utf-8

from typeclasses.rooms import Room
from commands.default_cmdsets import InstanceRoomCanBeSearchedCmdSet
from commands import command
import random


class InstanceRoom(Room):

    def at_object_creation(self):
        pass

class InstanceRoomCanBeExplored(InstanceRoom):
    """
    This room class is used by character-generation rooms. It makes
    the ChargenCmdset available.
    """
    BASE_MAGIC_FOUND = 0.5
    AVAILABLE_DROP_ITEMS = ["Longsword","Sharpsword"]

    def at_object_creation(self):
        self.cmdset.add(InstanceRoomCanBeSearchedCmdSet, permanent=True)
        # 掉落的物品存放在此
        self.db.drop_item_list = []
        # 可掉落的物品
        self.db.available_drop_items = self.AVAILABLE_DROP_ITEMS
        # 掉落物品品质几率
        self.db.drop_rate = self.BASE_MAGIC_FOUND

    def at_explore(self):
        self.db.drop_item_list.add(random.choice(self.db.available_drop_items))

#  兵器库
class BingQiKu(InstanceRoomCanBeExplored):
    """
    This room class is used by character-generation rooms. It makes
    the ChargenCmdset available.
    """
    BASE_MAGIC_FOUND = 0.5
    AVAILABLE_DROP_ITEMS = ["Money", "Longsword", "Sharpsword"]

    def at_object_creation(self):
        self.cmdset.add(InstanceRoomCanBeSearchedCmdSet, permanent=True)
        # 掉落的物品存放在此
        self.db.drop_item_list = []
        # 可掉落的物品
        self.db.available_drop_items = self.AVAILABLE_DROP_ITEMS
        # 掉落物品品质几率
        self.db.drop_rate = self.BASE_MAGIC_FOUND

    def at_explore(self):
        self.db.drop_item_list.add(random.choice(self.db.available_drop_items))
        self.db.drop_item_list.add(random.choice(self.db.available_drop_items))

