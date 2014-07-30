

from meatbot.status import User, Project, StatusUpdate

from random import randint

rint = lambda: randint(0, 100000000)


def test_get_user():
    i = rint()

    user = User.get_or_create(i)
    assert user is not None

    user2 = User.get_or_create(i)
    assert user == user2
