from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Integer, Column, Text

Base = declarative_base()
class TItems(Base):
    __tablename__ = 't_items'
    id = Column(Integer, primary_key = True, nullable = False, autoincrement = True)
    name = Column(String, nullable = False)
    image = Column(String, nullable = False)
    category = Column(Integer, nullable = False)
    count = Column(Integer, nullable = False)
    quantifier = Column(Integer, nullable = False)
    barcode = Column(String, nullable = True)
    description = Column(Text, nullable = False)
