from app.models.base import Base, db
from sqlalchemy import Column, String

class Currency(db.Model):
    __tablename__ = 'currencies'

    currency_name = Column(String, primary_key=True, comment='幣別名稱')