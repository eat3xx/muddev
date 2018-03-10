#coding=utf-8

from utils import general
from commands.command import Command

class CmdSkillFunc(Command):
    """
    通用技能命令，所有技能命令应继承此类，目的为重用func()方法
    所有技能命令只需定义key , aliases 即可
    """
    locks = "cmd:all()"
    help_category = "Skill"
    def func(self):
        caller = self.caller
        obj = self.obj
        if not self.args:
            self.caller.msg("Usage: %s %s" % (self.key, "enemy"))
            return
        target = caller.search(self.args.strip())
        obj.cast(caller, target)

class CmdZhongji(CmdSkillFunc):
    """
    技能: 重击
    """
    key = "zhongji"
    aliases = ["zhongji"]
    locks = "cmd: holds(基本拳脚)"

class CmdTaiZuBaShi(CmdSkillFunc):
    """
    技能: 太祖长拳
    """
    key = "taizubashi"
    aliases = ["taizubashi"]
    locks = "cmd: holds(太祖长拳)"
