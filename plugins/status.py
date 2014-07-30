from will.mixins import HipChatMixin
from will.plugin import WillPlugin
from will.decorators import respond_to

from pprint import pprint


from meatbot.status import User, Project, StatusUpdate


class StatusPlugin(WillPlugin, HipChatMixin):
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

        user = message.get_from()
        user_id = user.user.split("_")[1]
        hipchat_user = self.get_hipchat_user(user_id)

        # available on hipchat_user
        user = User.get_or_create(hipchat_user['id'])


        pprint(hipchat_user)

        print user.username
        self.reply(message, "bacon also to you... go in peace")


"""
session.query(User).filter(User.user_id == user_id)


"""
