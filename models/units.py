from models import Base
from sqlalchemy import Column, String

class Unit(Base):
    __tablename__ = 'units'

    unit_name = Column(String, primary_key=True, comment='單位名稱')