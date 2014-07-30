from sleekxmpp import Message
from will.mixins import HipChatMixin
from will.plugin import WillPlugin
from will.decorators import respond_to

from pprint import pprint


from meatbot.status import User, Project, StatusUpdate


def dump(obj):
    for x in dir(obj):
        print "%s:%s" % (x, getattr(obj, x))

class StatusPlugin(WillPlugin):

    def get_user(self, message):
        assert isinstance(message, Message)
        user = message.sender
        print type(user)
        # user_id = user.user.split("_")[1]
        # hipchat_user = self.get_hipchat_user(user_id)

        # available on hipchat_user
        user = User.get_or_create(user.hipchat_id,
                                  user.name,
                                  user.nick)
        return user

    @respond_to("mkproject (?P<project_name>.*)")
    def mkproject(self, message, project_name):
        user = self.get_user(message)
        self.reply(message, "Project %s created for you, %s" % (project_name, user.mention_name))

    @respond_to("test")
    def test(self, message):
        print message.sender
        user = self.get_user(message)


    @respond_to("!(.*):(.*)")
    def update_status(self, message):
        # insert into postgres
        print pprint(message)
        self.reply(message, "Status updated.")


    @respond_to("bacon")
    def bacon(self, message):
        """
        :type message sleekxmpp.stanza.message.Message
        """
        user = self.get_user(message)
        self.reply(message, "bacon also to you... go in peace")


"""
session.query(User).filter(User.user_id == user_id)


"""
