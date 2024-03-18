from models import Base
from sqlalchemy import Column, String
class Request_Type(Base):
    __tablename__ = 'request_types'

    type = Column(String, primary_key=True, comment='請購類型')