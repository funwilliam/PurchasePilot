from models import Base
from sqlalchemy import Column, String

class Currency(Base):
    __tablename__ = 'currencies'

    currency_name = Column(String, primary_key=True, comment='幣別名稱')