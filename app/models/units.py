from app.models.base import Base, db
from sqlalchemy import Column, String

class Unit(db.Model):
    __tablename__ = 'units'

    unit_name = Column(String, primary_key=True, comment='單位名稱')