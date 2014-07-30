

from meatbot.status import User, Project, StatusUpdate

from random import randint


rint = lambda: randint(0, 100000000) # random int

import uuid

def mkuser():
    i = rint()
    return User.get_or_create(i, "test", "test" + str(i))

def mkprojects(user, num=3):
    # shortcut to make a few projects for a test user
    tmp = []

    for x in range(num):
        Project.create(user.user_id, str(uuid.uuid4()))

    return tmp

def populate_project(project, items=3):
    for x in range(items):
        StatusUpdate.create(project.project_id, "test")




def test_get_user():
    i = rint()

    user = User.get_or_create(i, "pete", "bigpete" + (str(i)))
    assert user is not None

    sp = "smallpete%s" % str(i)
    user2 = User.get_or_create(i, "pete", sp)
    assert user == user2

    small_pete = User.get(i)
    assert small_pete.mention_name == sp

    pete = User.get_by_nick(sp)
    assert pete == small_pete


def test_mk_project():
    user = mkuser()



def test_get_updates():
    u1 = mkuser()
    u2 = mkuser()
    projects1 = mkprojects(u1, 2)
    projects2 = mkprojects(u2, 2)




