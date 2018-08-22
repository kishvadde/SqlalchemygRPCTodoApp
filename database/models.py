from sqlalchemy import Column,String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Todo(Base):
    
    __tablename__ = "todolist"
    id = Column('id',Integer, primary_key=True)
    name = Column('name',String, unique=True, nullable=False)
    is_completed = Column('is_completed', Boolean, nullable=False, default=False)
    is_active = Column('is_active', Boolean, nullable=False, default=True)

    def asdict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}