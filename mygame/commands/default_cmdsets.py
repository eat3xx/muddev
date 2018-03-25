#coding=utf-8
"""
Command sets

All commands in the game must be grouped in a cmdset.  A given command
can be part of any number of cmdsets and cmdsets can be added/removed
and merged onto entities at runtime.

To create new commands to populate the cmdset, see
`commands/command.py`.

This module wraps the default command sets of Evennia; overloads them
to add/remove commands from the default lineup. You can create your
own cmdsets by inheriting from them or directly from `evennia.CmdSet`.

"""

from evennia import default_cmds
from evennia import CmdSet
from commands import command
from commands import skillcommand

# 人物角色命令集： 查看属性，攻击，拾取战利品
class CharacterCmdSet(default_cmds.CharacterCmdSet):
    """
    The `CharacterCmdSet` contains general in-game commands like `look`,
    `get`, etc available on in-game Character objects. It is merged with
    the `AccountCmdSet` when an Account puppets a Character.
    """
    key = "DefaultCharacter"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super(CharacterCmdSet, self).at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
        self.add(command.CmdAbilities)
        self.add(command.CmdAttack)
        # self.add(command.CmdCreateNPC)
        # self.add(command.CmdEditNPC)
        self.add(command.CmdLoot)
        # self.add(command.CmdMobOnOff())
        # self.add(command.CmdSell)
        self.add(command.CmdEquipment)
        self.add(command.CmdInventory)
        self.add(command.CmdEquip)
        self.add(command.CmdPractise)
        self.add(command.CmdStudy)
        self.add(command.CmdBaseSkill)
        self.add(command.CmdSpecialSkill)
        self.add(command.CmdStop)
        self.add(command.CmdEquipSkill)

class AccountCmdSet(default_cmds.AccountCmdSet):
    """
    This is the cmdset available to the Account at all times. It is
    combined with the `CharacterCmdSet` when the Account puppets a
    Character. It holds game-account-specific commands, channel
    commands, etc.
    """
    key = "DefaultAccount"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super(AccountCmdSet, self).at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #


class UnloggedinCmdSet(default_cmds.UnloggedinCmdSet):
    """
    Command set available to the Session before being logged in.  This
    holds commands like creating a new account, logging in, etc.
    """
    key = "DefaultUnloggedin"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super(UnloggedinCmdSet, self).at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #


class SessionCmdSet(default_cmds.SessionCmdSet):
    """
    This cmdset is made available on Session level once logged in. It
    is empty by default.
    """
    key = "DefaultSession"

    def at_cmdset_creation(self):
        """
        This is the only method defined in a cmdset, called during
        its creation. It should populate the set with command instances.

        As and example we just add the empty base `Command` object.
        It prints some info.
        """
        super(SessionCmdSet, self).at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #


class ChargenCmdset(CmdSet):
    """
    This cmdset it used in character generation areas.
    """
    key = "Chargen"
    def at_cmdset_creation(self):
        "This is called at initialization"
        self.add(command.CmdSetPower())


class WeaponCmdSet(CmdSet):
    """Holds the attack command."""
    def at_cmdset_creation(self):
        pass

# 怪物的命令集： 攻击
class MonsterCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(command.CmdAttack())

# 装备的命令集： 装备，取下
class EquipmentCmdSet(CmdSet):
    def at_cmdset_creation(self):
        # self.add(command.CmdEquip())
        pass

# 物品的命令集：
class ObjectCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(command.CmdSell())
        pass

class MerchantRoomCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(command.CmdSell())

class InstanceRoomCmdSet(CmdSet):
    def at_cmdset_creation(self):
        # self.add(command.CmdSearch())
        pass

class InstanceRoomCanBeSearchedCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(command.CmdExplore())

class SkillCmdSet(CmdSet):
    def at_cmdset_creation(self):
        # self.add(skillcommand.CmdZhongji)
        pass

class BaseQuanJiaoCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(skillcommand.CmdZhongji)

class TaiZuChangQuanCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(skillcommand.CmdTaiZuBaShi)
