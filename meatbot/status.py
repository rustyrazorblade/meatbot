from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
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


class Project(Base):
    __tablename__ = 'project'
    project_id = Column(Integer, primary_key=True)
    name = Column(Text)



class StatusUpdate(Base):
    __tablename__ = 'status_update'
    status_update_id = Column(Integer, primary_key=True)


class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)

    @classmethod
    def get_or_create(cls, user_id):
        with session_scope() as session:
            user = session.query(User).filter(User.user_id==user_id).first()
            if not user:
                user = User(user_id=user_id)
                session.add(user)
        return user

    def __eq__(self, other):
        return other.user_id == self.user_id

