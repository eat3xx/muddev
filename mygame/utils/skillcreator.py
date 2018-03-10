#coding=utf-8

from evennia import create_object

def create_skill(caller, skill):
    create_object(skill.db.classpath,
                 key=skill.db.name,
                 location=caller,
                 locks="edit:id(%i) and perm(Builders);call:id(%i)" % (caller.id, caller.id))
