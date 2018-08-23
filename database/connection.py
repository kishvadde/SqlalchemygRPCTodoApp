from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from .models import Todo


@contextmanager
def db_session():
   
    engine  = create_engine('mysql+pymysql://root:@127.0.0.1/todolistdb')
    session = None
    if engine:
        session = sessionmaker(bind=engine)()
    yield session
    session.commit()
    session.close()