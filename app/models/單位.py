from app.models.base import Base, db
from sqlalchemy import Column, String

class 單位(db.Model):
    __tablename__ = '單位'

    代碼 = Column(String, primary_key=True)
    中文含意 = Column(String)
    英文含意 = Column(String)