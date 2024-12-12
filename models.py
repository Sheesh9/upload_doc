from sqlalchemy import Column, Integer, String
from database import Base, engine

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    filepath = Column(String)

# Создание таблиц в базе данных
def init_db():
    Base.metadata.create_all(bind=engine)