import uuid
from cqlengine.connection import setup
from cqlengine.management import sync_table, create_keyspace
from cqlengine import Model, UUID, Text, TimeUUID, DateTime, Integer

setup(["localhost"], "meatbot")


class User(Model):
    user_id = Integer(primary_key=True)
    name = Text()
    mention_name = Text()

    @classmethod
    def get_or_create(cls, user_id, name, mention_name):
        try:
            user = User.get(user_id)
        except:
            user = User.create(user_id=user_id,
                        name=name,
                        mention_name=mention_name)
        return user

    @classmethod
    def get_by_nick(cls, nick):
        for user in User.objects():
            if user.mention_name == nick:
                return user

        raise User.DoesNotExist

    def __eq__(self, other):
        return other.user_id == self.user_id

sync_table(User)



class ProjectAlreadyExistsException(Exception):
    def __init__(self, project_id):
        self.project_id = project_id

class Project(Model):
    user_id = Integer(primary_key=True)
    project_id = TimeUUID(primary_key=True, clustering_order='DESC', default=uuid.uuid1)
    name = Text()

    @classmethod
    def create(cls, user, name):
        try:
            p = Project.get_by_name(user, name)
        except:
            project = super(Project, cls).create(user_id=user.user_id, name=name)
        return project

sync_table(Project)


class StatusUpdate(Model):
    # status updates are per project
    project_id = UUID(primary_key=True)
    update_id = TimeUUID(primary_key=True, clustering_order='DESC', default=uuid.uuid1)
    user_id = Integer(required=True)
    message = Text()
    created_at = DateTime()

    @classmethod
    def create(cls, project, message):
        return super(StatusUpdate, cls).create(project_id=project.project_id,
                                               user_id=project.user_id,
                                               message=message)

    @classmethod
    def get_updates(cls, user=None, project=None, since=None):
        if not user:
            # all the users!
            users = User.objects()
            for user in users:
                # get each project
            pass
        return []


sync_table(StatusUpdate)


