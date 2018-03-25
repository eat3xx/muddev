#coding=utf-8
"""
Commands

Commands describe the input the account can do to the game.

"""

from evennia import Command as BaseCommand
from evennia import EvTable
from evennia import create_object

from settings.skilldef import SkillDefinition
from typeclasses.equipment.equipment import Equipment
from typeclasses.item.skill.huashan.skills import SpecialSkill
from typeclasses.item.skill.skill import Skill
from utils import general
from utils.general import determine_quality, get_equiped_equipments, get_equiped_equipment_by_type, \
    get_equiped_special_skill_by_type, holds
from utils.skillcreator import create_skill


class Command(BaseCommand):
    """
    Inherit from this if you want to create your own command styles
    from scratch.  Note that Evennia's default commands inherits from
    MuxCommand instead.

    Note that the class's `__doc__` string (this text) is
    used by Evennia to create the automatic help entry for
    the command, so make sure to document consistently here.

    Each Command implements the following methods, called
    in this order (only func() is actually required):
        - at_pre_cmd(): If this returns True, execution is aborted.
        - parse(): Should perform any extra parsing needed on self.args
            and store the result on self.
        - func(): Performs the actual work.
        - at_post_cmd(): Extra actions, often things done after
            every command, like prompts.

    """
    pass

# -------------------------------------------------------------
#
# The default commands inherit from
#
#   evennia.commands.default.muxcommand.MuxCommand.
#
# If you want to make sweeping changes to default commands you can
# uncomment this instance of the MuxCommand parent and add
#
#   COMMAND_DEFAULT_CLASS = "commands.command.MuxCommand"
#
# to your settings file. Be warned that the default commands expect
# the functionality implemented in the parse() method, so be
# careful with what you change.
#
# -------------------------------------------------------------

# from evennia.utils import utils
#
#
# class MuxCommand(Command):
#     """
#     This sets up the basis for a MUX command. The idea
#     is that most other Mux-related commands should just
#     inherit from this and don't have to implement much
#     parsing of their own unless they do something particularly
#     advanced.
#
#     Note that the class's __doc__ string (this text) is
#     used by Evennia to create the automatic help entry for
#     the command, so make sure to document consistently here.
#     """
#     def has_perm(self, srcobj):
#         """
#         This is called by the cmdhandler to determine
#         if srcobj is allowed to execute this command.
#         We just show it here for completeness - we
#         are satisfied using the default check in Command.
#         """
#         return super(MuxCommand, self).has_perm(srcobj)
#
#     def at_pre_cmd(self):
#         """
#         This hook is called before self.parse() on all commands
#         """
#         pass
#
#     def at_post_cmd(self):
#         """
#         This hook is called after the command has finished executing
#         (after self.func()).
#         """
#         pass
#
#     def parse(self):
#         """
#         This method is called by the cmdhandler once the command name
#         has been identified. It creates a new set of member variables
#         that can be later accessed from self.func() (see below)
#
#         The following variables are available for our use when entering this
#         method (from the command definition, and assigned on the fly by the
#         cmdhandler):
#            self.key - the name of this command ('look')
#            self.aliases - the aliases of this cmd ('l')
#            self.permissions - permission string for this command
#            self.help_category - overall category of command
#
#            self.caller - the object calling this command
#            self.cmdstring - the actual command name used to call this
#                             (this allows you to know which alias was used,
#                              for example)
#            self.args - the raw input; everything following self.cmdstring.
#            self.cmdset - the cmdset from which this command was picked. Not
#                          often used (useful for commands like 'help' or to
#                          list all available commands etc)
#            self.obj - the object on which this command was defined. It is often
#                          the same as self.caller.
#
#         A MUX command has the following possible syntax:
#
#           name[ with several words][/switch[/switch..]] arg1[,arg2,...] [[=|,] arg[,..]]
#
#         The 'name[ with several words]' part is already dealt with by the
#         cmdhandler at this point, and stored in self.cmdname (we don't use
#         it here). The rest of the command is stored in self.args, which can
#         start with the switch indicator /.
#
#         This parser breaks self.args into its constituents and stores them in the
#         following variables:
#           self.switches = [list of /switches (without the /)]
#           self.raw = This is the raw argument input, including switches
#           self.args = This is re-defined to be everything *except* the switches
#           self.lhs = Everything to the left of = (lhs:'left-hand side'). If
#                      no = is found, this is identical to self.args.
#           self.rhs: Everything to the right of = (rhs:'right-hand side').
#                     If no '=' is found, this is None.
#           self.lhslist - [self.lhs split into a list by comma]
#           self.rhslist - [list of self.rhs split into a list by comma]
#           self.arglist = [list of space-separated args (stripped, including '=' if it exists)]
#
#           All args and list members are stripped of excess whitespace around the
#           strings, but case is preserved.
#         """
#         raw = self.args
#         args = raw.strip()
#
#         # split out switches
#         switches = []
#         if args and len(args) > 1 and args[0] == "/":
#             # we have a switch, or a set of switches. These end with a space.
#             switches = args[1:].split(None, 1)
#             if len(switches) > 1:
#                 switches, args = switches
#                 switches = switches.split('/')
#             else:
#                 args = ""
#                 switches = switches[0].split('/')
#         arglist = [arg.strip() for arg in args.split()]
#
#         # check for arg1, arg2, ... = argA, argB, ... constructs
#         lhs, rhs = args, None
#         lhslist, rhslist = [arg.strip() for arg in args.split(',')], []
#         if args and '=' in args:
#             lhs, rhs = [arg.strip() for arg in args.split('=', 1)]
#             lhslist = [arg.strip() for arg in lhs.split(',')]
#             rhslist = [arg.strip() for arg in rhs.split(',')]
#
#         # save to object properties:
#         self.raw = raw
#         self.switches = switches
#         self.args = args.strip()
#         self.arglist = arglist
#         self.lhs = lhs
#         self.lhslist = lhslist
#         self.rhs = rhs
#         self.rhslist = rhslist
#
#         # if the class has the account_caller property set on itself, we make
#         # sure that self.caller is always the account if possible. We also create
#         # a special property "character" for the puppeted object, if any. This
#         # is convenient for commands defined on the Account only.
#         if hasattr(self, "account_caller") and self.account_caller:
#             if utils.inherits_from(self.caller, "evennia.objects.objects.DefaultObject"):
#                 # caller is an Object/Character
#                 self.character = self.caller
#                 self.caller = self.caller.account
#             elif utils.inherits_from(self.caller, "evennia.accounts.accounts.DefaultAccount"):
#                 # caller was already an Account
#                 self.character = self.caller.get_puppet(self.session)
#             else:
#                 self.character = None
class CmdAbilities(Command):
    """
    List abilities

    Usage:
      abilities

    Displays a list of your current ability values.
    """
    key = "abilities"
    aliases = ["abi"]
    lock = "cmd:all()"
    help_category = "General"

    def func(self):
        "implements the actual functionality"

        level, strength, agility, stamina, health = self.caller.get_abilities()
        string = "Level %s, Strength: %s, Agility: %s, Stamina %s, Health %s" % (level, strength, agility, stamina, health)
        self.caller.msg(string)

class CmdSetPower(Command):
    """
    set the power of a character

    Usage:
      +setpower <1-10>

    This sets the power of the current character. This can only be
    used during character generation.
    """

    key = "+setpower"
    help_category = "mush"

    def func(self):
        "This performs the actual command"
        errmsg = "You must supply a number between 1 and 10."
        if not self.args:
            self.caller.msg(errmsg)
            return
        try:
            power = int(self.args)
        except ValueError:
            self.caller.msg(errmsg)
            return
        if not (1 <= power <= 10):
            self.caller.msg(errmsg)
            return
        # at this point the argument is tested as valid. Let's set it.
        self.caller.db.power = power
        self.caller.msg("Your Power was set to %i." % power)

class CmdAttack(Command):
    key = "attack"
    aliases = ["att"]
    lock = "cmd:all()"
    help_category = "mush"

    def func(self):
        caller = self.caller
        if not self.args:
            caller.msg("Usage: %s %s" % (self.key, "target"))
            return
        target = caller.search(self.args.strip())
        if not target:
            return
        if not target.ndb.is_immortal:
            caller.db.current_enemy = target
            caller.start_attacking()
        else:
            caller.msg("不可攻击该目标")

class CmdEquip(Command):
    key = "equip"
    aliases = ["unequip"]
    help_category = "mush"
    arg_regex = r"\s|$"

    def func(self):
        caller = self.caller
        if not self.args:
            caller.msg("Usage: %s %s" % (self.key, "target"))
            return
        target = caller.search(self.args.strip())
        if not target:
            return
        if self.cmdstring == "equip":
            # 得到人物当前同等位置装备，如果有则先取下
            equipment = get_equiped_equipment_by_type(caller, target.db.type)
            if equipment:
                # put_on_equipment(caller, equipment, reverse=True)
                equipment.at_equip(caller, equip=False)
            caller.msg("你装备上了%s" % target)
            target.at_equip(caller, equip=True)
        else:
            caller.msg("你脱下了%s" % target)
            target.at_equip(caller, equip=False)

class CmdSell(Command):
    key = "sell"
    aliases = ["sell"]
    lock = "cmd:all()"
    help_category = "mush"

    def func(self):
        caller = self.caller
        if not self.args:
            caller.msg("Usage: %s %s" % (self.key, "target"))
            return
        target = caller.search(self.args.strip())
        # target = self.args.strip()
        if not target:
            return

        if target.db.is_equiped == True:
            self.caller.msg("售卖前请先取下装备")
            return
        target.delete()
        cmd_string = "del/force"
        # print "%s %s" % (cmd_string, target)
        # print "%s %s" % (cmd_string, target.key)
        # target_str = "#"+str(target.id)
        # print "%s %s" % (cmd_string, target_str)
        # caller.execute_cmd("%s %s" % (cmd_string, target_str))

class CmdCreateNPC(Command):
    """
    create a new npc

    Usage:
        +createNPC <name>

    Creates a new, named NPC. The NPC will start with a Power of 1.
    """
    key = "+createnpc"
    aliases = ["+createNPC"]
    locks = "call:not perm(nonpcs)"
    help_category = "mush"

    def func(self):
        "creates the object and names it"
        caller = self.caller
        if not self.args:
            caller.msg("Usage: +createNPC <name>")
            return
        if not caller.location:
            # may not create npc when OOC
            caller.msg("You must have a location to create an npc.")
            return
        # make name always start with capital letter
        name = self.args.strip().capitalize()
        # create npc in caller's location
        npc = create_object("chars.Character",
                            key=name,
                            location=caller.location,
                            locks="edit:id(%i) and perm(Builders);call:false()" % caller.id)
        # announce
        message = "%s created the NPC '%s'."
        caller.msg(message % ("You", name))
        caller.location.msg_contents(message % (caller.key, name),
                                     exclude=caller)

class CmdEditNPC(Command):
    """
    edit an existing NPC

    Usage:
      +editnpc <name>[/<attribute> [= value]]

    Examples:
      +editnpc mynpc/power = 5
      +editnpc mynpc/power    - displays power value
      +editnpc mynpc          - shows all editable
                                attributes and values

    This command edits an existing NPC. You must have
    permission to edit the NPC to use this.
    """
    key = "+editnpc"
    aliases = ["+editNPC"]
    locks = "cmd:not perm(nonpcs)"
    help_category = "mush"

    def parse(self):
        "We need to do some parsing here"
        args = self.args
        propname, propval = None, None
        if "=" in args:
            args, propval = [part.strip() for part in args.rsplit("=", 1)]
        if "/" in args:
            args, propname = [part.strip() for part in args.rsplit("/", 1)]
        # store, so we can access it below in func()
        self.name = args
        self.propname = propname
        # a propval without a propname is meaningless
        self.propval = propval if propname else None

    def func(self):
        "do the editing"

        allowed_propnames = ("power", "attribute1", "attribute2")

        caller = self.caller
        if not self.args or not self.name:
            caller.msg("Usage: +editnpc name[/propname][=propval]")
            return
        npc = caller.search(self.name)
        if not npc:
            return
        if not npc.access(caller, "edit"):
            caller.msg("You cannot change this NPC.")
            return
        if not self.propname:
            # this means we just list the values
            output = "Properties of %s:" % npc.key
            for propname in allowed_propnames:
                propvalue = npc.attributes.get(propname, default="N/A")
                output += "\n %s = %s" % (propname, propvalue)
            caller.msg(output)
        elif self.propname not in allowed_propnames:
            caller.msg("You may only change %s." %
                       ", ".join(allowed_propnames))
        elif self.propval:
            # assigning a new propvalue
            # in this example, the properties are all integers...
            intpropval = int(self.propval)
            npc.attributes.add(self.propname, intpropval)
            caller.msg("Set %s's property '%s' to %s" %
                       (npc.key, self.propname, self.propval))
        else:
            # propname set, but not propval - show current value
            caller.msg("%s has property %s = %s" %
                       (npc.key, self.propname,
                        npc.attributes.get(self.propname, default="N/A")))

class CmdLoot(Command):
    """
    拾取战利品，用于战斗后从目标身上拾取物品
    用法: loot target
    """
    key = "+loot"
    aliases = ["loot"]
    locks = "cmd:all()"
    help_category = "mush"

    def func(self):
        # 没有提供目标参数，退出
        if not self.args:
            self.caller.msg("Usage: %s %s" % (self.key, "target"))
            return
        target = self.caller.search(self.args.strip())

        # 目标不存在或者目标已经死亡或者目标不在当前场景，则返回
        if not target:
            self.caller.msg("无法拾取，%s 不存在" % target.key)
            return
        if not target.db.is_dead:
            self.caller.msg("无法拾取，%s 未死亡" % target.key)
            return
        if target.location != self.caller.location:
            self.caller.msg("无法拾取，%s 距离过远" % target.key)
            return

        # 获取目标掉落物品列表
        items = target.db.drop_item_list
        # 清空目标掉落物品列表
        target.db.drop_item_list = []
        if not items:
            self.caller.msg("对方没有掉落任何物品")
            return
        for item in items:
            # 生成基础物品类型
            item_created = create_object(item.get("classpath"),
                                 # key = "长剑",
                                 key = item.get("name"),
                                 # key=item.split(".")[-1],
                                 location=self.caller,
                                 # locks="edit:id(%i) and perm(Builders)" % self.caller.id)
                                 locks="edit:id(%i) and perm(Builders);call:id(%i)" % (self.caller.id, self.caller.id))
            item_created.key = item_created.db.name
            # 决定最终掉率
            rate_target = target.db.drop_rate
            rate_caller = self.caller.db.magic_found
            rate = rate_target * (1 + rate_caller/100.00)

            # 根据掉率决定最终品质
            quality = determine_quality(rate)

            # 将品质附加到物品上，加强物品属性
            item_created.set_quality(quality)

            self.caller.msg("你获得了" + item_created.key)

class CmdMobOnOff(Command):
    """
    Activates/deactivates Mob

    Usage:
        mobon <mob>
        moboff <mob>

    This turns the mob from active (alive) mode
    to inactive (dead) mode. It is used during
    building to  activate the mob once it's
    prepared.
    """
    key = "mobon"
    aliases = "moboff"
    locks = "cmd:superuser()"
    help_category = "monster"

    def func(self):
        """
        Uses the mob's set_alive/set_dead methods
        to turn on/off the mob."
        """
        if not self.args:
            self.caller.msg("Usage: mobon|moboff <mob>")
            return
        mob = self.caller.search(self.args)
        if not mob:
            return
        if self.cmdstring == "mobon":
            mob.set_alive()
        else:
            mob.set_dead()

class CmdInventory(Command):
    """
    view inventory

    Usage:
      inventory
      inv

    Shows your inventory.
    """
    key = "inventory"
    aliases = ["inv", "i"]
    locks = "cmd:all()"
    arg_regex = r"$"

    def func(self):
        """check inventory"""
        items = self.caller.contents
        if not items:
            string = "你包里什么物品都没有\n"
        else:
            table = EvTable(border="header")
            for item in items:
                if not item.db.is_equiped and not isinstance(item, Skill):
                    table.add_row("%s%s|n" % (item.db.color, item.name), item.db.desc or "")
            string = "|w背包里的物品:\n%s" % table + "\n"
        string += general.show_me_the_money(self.caller.db.money)
        self.caller.msg(string)

class CmdEquipment(Command):
    """
    view inventory

    Usage:
      inventory
      inv

    Shows your inventory.
    """
    key = "equipment"
    aliases = ["equipment"]
    locks = "cmd:all()"
    arg_regex = r"$"

    def func(self):
        """check inventory"""
        caller = self.caller
        equipments = get_equiped_equipments(caller)
        if not equipments:
            string = "你没有装备任何东西"
        else:
            table = EvTable(border="header")
            for item in equipments:
                if isinstance(item, Equipment):
                    table.add_row("|C%s|n" % item.name, item.db.desc or "")
            string = "|w你身上的装备:\n%s" % table
        self.caller.msg(string)

class CmdStudy(Command):
    """
    学习技能

    Usage:
    learn jibenquanjiao master

    跟师傅学习技能
    """
    key = "study"
    aliases = ["study"]
    locks = "cmd:all()"
    help_category = "mush"

    def parse(self):
        if not self.args:
            self.caller.msg("Usage: %s %s %s" % (self.key, "skill", "master"))
            return
        args = self.args.strip()
        self.skill, self.master = [part.strip() for part in args.rsplit()]

    def func(self):
        caller = self.caller
        if not self.args:
            self.caller.msg("Usage: %s %s" % (self.key, "master"))
            return

        skill_dict = SkillDefinition.get_skill_by_name(self.skill)
        skill_classpath = skill_dict.get("classpath")
        if holds(caller, self.skill):
            pass
        else:
            create_object(skill_classpath,
                          key=self.skill,
                          location=caller,
                          locks="edit:id(%i) and perm(Builders);call:id(%i)" % (caller.id, caller.id))
        skill = caller.search(self.skill.strip())
        master = caller.search(self.master.strip())
        if skill and master:
            caller.start_studying(skill, master)

class CmdPractise(Command):
    """
    练习技能

    Usage:
    practise jibenquanjiao

    练习技能
    """
    key = "practise"
    aliases = ["practise"]
    locks = "cmd:all()"
    help_category = "mush"

    def func(self):
        caller = self.caller
        if not self.args:
            self.caller.msg("Usage: %s %s" % (self.key, "target"))
            return
        target = caller.search(self.args.strip())
        caller.start_pracising(target)

class CmdExplore(Command):
    key = "explore"
    aliases = ["explore"]
    locks = "cmd:all()"
    help_category = "room"

    def func(self):
        # 没有提供目标参数，退出
        if not self.args:
            self.caller.msg("Usage: %s %s" % (self.key, "location"))
            return
        target = self.caller.search(self.args.strip())

        target.at_explore()

        # 获取目标掉落物品列表
        items = target.db.drop_item_list
        # 清空目标掉落物品列表
        target.db.drop_item_list = []
        if not items:
            self.caller.msg("没有找到任何东西")
            return
        for item in items:
            # 生成基础物品类型
            item_created = create_object("typeclasses.equipment.weapon.sword." + item,
                                 key=item,
                                 location=self.caller,
                                 # locks="edit:id(%i) and perm(Builders)" % self.caller.id)
                                 locks="edit:id(%i) and perm(Builders);call:id(%i)" % (self.caller.id, self.caller.id))
            # 决定物品品质
            rate_target = target.db.drop_rate
            rate_caller = self.caller.db.magic_found
            rate = rate_target * (1 + rate_caller/100.00)
            # 根据掉率决定最终品质
            quality = determine_quality(rate)
            # 将品质附加到物品上，加强物品属性
            item_created.set_quality(quality)

            self.caller.msg("你获得了" + item_created.key)

class CmdEquipSkill(Command):
    """
    装备武功

    Usage:
    equipskill skillname
    """
    key = "equipskill"
    aliases = ["unequipskill"]
    locks = "cmd:all()"
    help_category = "mush"

    def func(self):
        caller = self.caller
        if not self.args:
            self.caller.msg("Usage: %s %s" % (self.key, "skillname"))
            return
        target = caller.search(self.args.strip())
        if not target or not isinstance(target, SpecialSkill):
            caller.msg("你只能装备或者卸下特殊武功")
            return
        if self.cmdstring == "equipskill":
            # 得到人物当前同等位置技能，如果有则先卸载
            if target.db.is_equiped == True:
                caller.msg("你不能重复装备已装备的武功")
                return
            special_skill = get_equiped_special_skill_by_type(caller, target.db.type)
            if special_skill:
                special_skill.at_equip(caller, equip=False)
            target.at_equip(caller, equip=True)
            caller.msg("已装备%s为%s" % (target.db.name, target.db.type))
        else:
            if target.db.is_equiped == False:
                caller.msg("你无法卸载为装备的武功")
                return
            caller.msg("已卸载%s" % target.db.name)
            target.at_equip(caller, equip=False)

class CmdBaseSkill(Command):
    """
    view inventory

    Usage:
      inventory
      inv

    Shows your inventory.
    """
    key = "baseskill"
    aliases = ["baseskill"]
    locks = "cmd:all()"
    arg_regex = r"$"

    def func(self):
        """check inventory"""
        caller = self.caller
        items = general.get_all_base_skills(caller)
        if not items:
            string = "你目前未掌握任何基础武功"
        else:
            table = EvTable(border="header")
            for item in items:
                table.add_row("%s%s|n" % (item.db.color, item.name), str(item.db.level) + "级/" + item.db.level_desc or "")
            string = "|w你掌握的基础武功:\n%s" % table
        self.caller.msg(string)

class CmdSpecialSkill(Command):
    """
    view inventory

    Usage:
      inventory
      inv

    Shows your inventory.
    """
    key = "specialskill"
    aliases = ["specialskill"]
    locks = "cmd:all()"
    arg_regex = r"$"

    def func(self):
        """check inventory"""
        caller = self.caller
        items = general.get_all_special_skills(caller)
        if not items:
            string = "你目前未掌握任何特殊武功"
        else:
            table = EvTable(border="header")
            for item in items:
                if item.db.is_equiped == True:
                    equiped = "(已装备为%s)" % item.db.type
                    table.add_row("|C%s|n" % item.name, str(item.db.level) + "级/" + item.db.level_desc, equiped or "")
                else:
                    table.add_row("%s%s|n" % (item.db.color, item.name), str(item.db.level) + "级/" + item.db.level_desc or "")
            string = "|w你掌握的特殊武功:\n%s" % table
        self.caller.msg(string)

class CmdStop(Command):
    """
    停止当前动作

    Usage:
    stop

    """
    key = "stop"
    aliases = ["stop"]
    locks = "cmd:all()"
    help_category = "mush"

    def func(self):
        caller = self.caller
        caller.start_idle()