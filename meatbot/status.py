from gevent.monkey import patch_all

import uuid
from datetime import datetime
from cqlengine.connection import setup
from cqlengine.management import sync_table
from cqlengine import Model, UUID, Text, TimeUUID, DateTime, Integer

import logging
logging.basicConfig()

connected = False


def connect():
    if connected: return
    print "Connecting"
    setup(["localhost"], "meatbot")
    print "Connected"
    sync_table(User)
    sync_table(Project)
    sync_table(StatusUpdate)
    sync_table(StatusUpdateUserAggregated)
    print "Done Syncing"
    global connected
    connected = True


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


import re

name_regex = re.compile("^[a-zA-Z0-9\-\_]+$")


class ProjectAlreadyExistsException(Exception): pass
class InvalidNameException(Exception): pass

class Project(Model):
    user_id = Integer(primary_key=True)
    name = Text(primary_key=True)

    @classmethod
    def create(cls, user, name):
        name = name.strip()
        if not name_regex.match(name):
            raise InvalidNameException()

        try:
            p = Project.get_by_name(user, name)
            raise ProjectAlreadyExistsException()
        except Project.DoesNotExist:
            project = super(Project, cls).create(user_id=user.user_id, name=name)
            return project

    @classmethod
    def get_by_name(cls, user, name):
        name = name.strip()
        return Project.get(user_id=user.user_id, name=name)




class StatusUpdate(Model):
    # status updates are per project
    project_name = Text(primary_key=True)
    update_id = TimeUUID(primary_key=True, clustering_order='DESC', default=uuid.uuid1)
    user_id = Integer(required=True)
    message = Text()
    created_at = DateTime(default=datetime.now)

    @classmethod
    def create(cls, project, message):
        tmp = super(StatusUpdate, cls).create(project_name=project.name,
                                               user_id=project.user_id,
                                               message=message)

        StatusUpdateUserAggregated.create(user_id=project.user_id,
                                   update_id=tmp.update_id,
                                   message=message,
                                   project=project.name,
                                   created_at=tmp.created_at)
        return tmp

    @classmethod
    def get_updates(cls, user=None, project=None, since=None):
        if not user:
            # all the users!
            users = User.objects()
            for user in users:
                # get each project
                pass
        return []

class StatusUpdateUserAggregated(Model):
    user_id = Integer(primary_key=True)
    update_id = TimeUUID(primary_key=True, clustering_order='DESC')
    project = Text(required=True)
    message = Text(required=True)
    created_at = DateTime(required=True)


