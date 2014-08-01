from sleekxmpp import Message
from will.plugin import WillPlugin
from will.decorators import respond_to, rendered_template

from meatbot.status import User, Project, StatusUpdate, ProjectAlreadyExistsException, connect, InvalidNameException, \
    StatusUpdateUserAggregated


def dump(obj):
    for x in dir(obj):
        print "%s:%s" % (x, getattr(obj, x))

class StatusPlugin(WillPlugin):


    def get_user(self, message):
        connect()
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
            Project.create(user, project_name)
            self.reply(message, "Project %s created for you, %s" % (project_name, user.mention_name))
        except ProjectAlreadyExistsException as e:
            self.reply(message, "Sorry, but that project already exists under your name.")
        except InvalidNameException:
            self.reply(message, "Sorry, just letters and numbers (no spaces).")

    @respond_to("lsp(?P<nick> .*)?")
    def lsproject(self, message, nick):
        # lists all projects, current user is assumed
        connect()
        if nick:
            nick = nick.strip()
            user = User.get_by_nick(nick)
        else:
            user = self.get_user(message)

        if not user:
            self.reply(message, "Could not find user %s" % nick)
            return

        projects = Project.objects(user_id=user.user_id)

        template = rendered_template("lsproject.html", {"user":user, "projects":projects})
        self.reply(message, template, html=True)


    @respond_to("update (?P<project_name>.+?) (?P<status>.+)")
    def update_status(self, message, project_name, status):
        connect()
        # insert into postgres
        user = self.get_user(message)

        try:
            project = Project.get(user_id=user.user_id, name=project_name)
        except Project.DoesNotExist:
            self.reply(message, "Sorry, project %s not found." % project_name)
            return

        status = StatusUpdate.create(project, status)

        self.reply(message, "Status updated." + str(status))

    @respond_to("help")
    def help(self, message):
        help_text = rendered_template("status_help.html", {})
        self.reply(message, help_text, html=True)



    @respond_to("^wtf ?(?P<nick>.*)")
    def show_updates(self, message, nick):
        # shows updates for a single user
        connect()
        try:
            if not nick:
                user = self.get_user(message)
            else:
                user = User.get_by_nick(nick)
        except User.DoesNotExist:
            self.reply(message, "%s does not exist yet." % nick)
            return


        updates = StatusUpdateUserAggregated.objects(user_id=user.user_id).limit(10)

        template = rendered_template("show_updates.html",
                                     {"user":user, "updates":updates})

        self.reply(message, template, html=True)


    @respond_to("^(derp|huh|meat)$")
    def summary_view(self, message):
        connect()
        result = []

        for user in User.objects():
            updates = StatusUpdateUserAggregated.objects(user_id=user.user_id).limit(10)

            template = rendered_template("show_updates.html",
                                         {"user":user, "updates":updates})
            result.append(template)

        response = "<BR>".join(result)
        self.reply(message, response, html=True)




class CuredMeats(WillPlugin):
    @respond_to("^bacon")
    def bacon(self):
        self.say("<img src='http://upload.wikimedia.org/wikipedia/commons/3/31/Made20bacon.png'>", html=True)
