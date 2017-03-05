from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class TCategories(Base):
    __tablename__ = 't_categories'
    
    id = Column(Integer, primary_key = True, autoincrement = True,  nullable = False)
    name = Column(String, nullable = False)
    parent = Column(Integer, nullable = False)
    icon = Column(String, nullable = True)
