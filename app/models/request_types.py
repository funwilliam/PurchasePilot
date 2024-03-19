from app.models.base import Base, db
from sqlalchemy import Column, String
class Request_Type(db.Model):
    __tablename__ = 'request_types'

    type = Column(String, primary_key=True, comment='請購類型')