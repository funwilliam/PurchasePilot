from app.models.base import Base, db
from sqlalchemy import Column, String

class 單位(db.Model):
    __tablename__ = '單位'

    單位名稱 = Column(String, primary_key=True)