#coding=utf-8

from typeclasses.objects import Object
from commands.default_cmdsets import EquipmentCmdSet

class Equipment(Object):

    def at_object_creation(self):
        super(Equipment, self).at_object_creation()
        self.cmdset.add(EquipmentCmdSet, permanent=True)

        self.db.is_equiped = False


    def reset(self):
        """
        销毁武器
        """
        if self.location.has_account and self.home == self.location:
            self.location.msg_contents("%s 消失了，就好像从未存在过 ..." % self.key)
            self.delete()
        else:
            self.location = self.home
