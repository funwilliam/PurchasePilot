from app.models.base import db
from sqlalchemy import Column, String

class 物料類別(db.Model):
    __tablename__ = '物料類別'

    類別 = Column(String, primary_key=True)