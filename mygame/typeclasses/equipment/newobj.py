from typeclasses.objects import Object
from commands.default_cmdsets import EquipmentCmdSet

class NewObj(Object):

    def at_object_creation(self):
        super(NewObj, self).at_object_creation()
        self.cmdset.add(EquipmentCmdSet, permanent=True)

        self.db.is_equiped = False