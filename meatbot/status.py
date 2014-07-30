from sqlalchemy import create_engine, Column, Integer, Text, Boolean, ForeignKey
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


    def __eq__(self, other):
        return other.user_id == self.user_id


class Project(Base):
    __tablename__ = 'project'
    project_id = Column(Integer, primary_key=True)
    name = Column(Text)
    active = Column(Boolean)
    user_id = Column(Integer, ForeignKey('user.user_id'))


class StatusUpdate(Base):
    __tablename__ = 'status_update'
    status_update_id = Column(Integer, primary_key=True)

