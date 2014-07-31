from sleekxmpp import Message
from will.plugin import WillPlugin
from will.decorators import respond_to, rendered_template

from meatbot.status import User, Project, StatusUpdate, ProjectAlreadyExistsException, connect


def dump(obj):
    for x in dir(obj):
        print "%s:%s" % (x, getattr(obj, x))

class StatusPlugin(WillPlugin):
    def get_user(self, message):
        assert isinstance(message, Message)
        user = message.sender
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
        try:
            Project.create(user.user_id, project_name)
            self.reply(message, "Project %s created for you, %s" % (project_name, user.mention_name))
        except ProjectAlreadyExistsException as e:
            self.reply(message, "Sorry, but that project already exists (id=%d)")

    @respond_to("lsp(?P<nick> .*)?")
    def lsproject(self, message, nick):
        # lists all projects, current user is assumed

        if nick:
            nick = nick.strip()
            user = User.get_by_nick(nick)
        else:
            user = self.get_user(message)

        if not user:
            self.reply(message, "Could not find user %s" % nick)
            return

        projects = Project.get_by_user(user)

        template = rendered_template("lsproject.html", {"user":user, "projects":projects})
        self.reply(message, template, html=True)


    @respond_to("test")
    def test(self, message):
        connect()
        print message.sender
        user = self.get_user(message)
        self.reply(message, "got it")


    @respond_to("update (?P<project_name>.+?) (?P<status>.+)")
    def update_status(self, message, project_name, status):
        # insert into postgres
        user = self.get_user(message)
        project = Project.get_by_user_and_name(user, project_name)

        if not project:
            self.reply(message, "Sorry, project %s not found." % project_name)
            return

        status = StatusUpdate.create(project.project_id, status)

        self.reply(message, "Status updated." + str(status))

    @respond_to("^wtf ?(?P<nick>.*)")
    def show_updates(self, message, nick):
        if not nick:
            self.reply(message, "YOU")
        else:
            self.reply(message, nick)

        template = rendered_template("show_updates.html", {})
        self.reply(message, template, html=True)


class CuredMeats(WillPlugin):
    @respond_to("bacon")
    def bacon(self):
        self.say("<img src='http://upload.wikimedia.org/wikipedia/commons/3/31/Made20bacon.png'>", html=True)
