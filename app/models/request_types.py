from app.models.base import Base, db
from sqlalchemy import Column, String
class 請購類型(db.Model):
    __tablename__ = '請購類型'

    類型 = Column(String, primary_key=True)