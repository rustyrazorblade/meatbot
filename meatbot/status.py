from sqlalchemy import create_engine, Column, Integer, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from contextlib import contextmanager


engine = create_engine("postgresql://jhaddad:@localhost/meatbot")
Base = declarative_base()

Session = sessionmaker(bind=engine, expire_on_commit=False)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()



class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    name = Column(Text)
    mention_name = Column(Text)

    projects = relationship("Project")

    @classmethod
    def get_or_create(cls, user_id, name, mention_name):
        with session_scope() as session:
            user = session.query(User).filter(User.user_id==user_id).first()
            if user:
                if user.name != name or user.mention_name != mention_name:
                    user.name = name
                    user.mention_name = mention_name
                    session.add(user)
            else:
                user = User(user_id=user_id, name=name, mention_name=mention_name)
                session.add(user)
        return user

    @classmethod
    def get(cls, user_id):
        with session_scope() as session:
            return session.query(User).filter(User.user_id==user_id).first()

    @classmethod
    def get_by_nick(cls, nick):
        with session_scope() as s:
            return s.query(User).filter(User.mention_name==nick).first()

    def __eq__(self, other):
        return other.user_id == self.user_id


class ProjectAlreadyExistsException(Exception):
    def __init__(self, project_id):
        self.project_id = project_id

class Project(Base):
    __tablename__ = 'project'
    project_id = Column(Integer, primary_key=True)
    name = Column(Text)
    active = Column(Boolean)
    user_id = Column(Integer, ForeignKey('user.user_id'))

    @classmethod
    def create(cls, user_id, name):
        with session_scope() as s:
            existing = s.query(Project).filter(Project.user_id==user_id).filter(Project.name == name).first()
            print existing
            if existing:
                raise ProjectAlreadyExistsException()
            p = Project(user_id=user_id, name=name)
            s.add(p)
        return p

    @classmethod
    def get_by_user(cls, user):
        with session_scope() as s:
            return s.query(Project).filter(Project.user_id==user.user_id).all()

    @classmethod
    def get_by_user_and_name(cls, user, name):
        with session_scope() as s:
            return s.query(Project).filter(Project.user_id == user.user_id).filter(Project.name==name).first()


class StatusUpdate(Base):
    __tablename__ = 'status_update'
    status_update_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('project.project_id'))
    message = Column(Text)
    created_at = Column(DateTime)

    @classmethod
    def create(cls, project_id, message):
        with session_scope() as s:
            status = StatusUpdate(project_id=project_id, message=message)
            s.add(status)

        return status

    def __str__(self):
        return "<StatusUpdate status_update_id=%d project_id=%d message=%s>" % (self.status_update_id, self.project_id, self.message)


    @classmethod
    def get_updates(cls, user=None, since=None):
        if since is None:
            # set to 1 day ago
            pass
        with session_scope() as s:
            tmp = s.query(StatusUpdate)

            return tmp.all()
