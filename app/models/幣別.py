from app.models.base import db
from sqlalchemy import Column, String

class 幣別(db.Model):
    __tablename__ = '幣別'

    代號 = Column(String, primary_key=True)
    名稱 = Column(String)
    維運組織 = Column(String)