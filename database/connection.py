from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from .models import Todo


@contextmanager
def db_session():
    engine  = create_engine('sqlite:///todolist.sqlite')
    session = None
    if engine:
        session = sessionmaker(bind=engine)()
    yield session
    session.commit()
    session.close()