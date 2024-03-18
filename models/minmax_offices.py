from models import Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class Office(Base):
    __tablename__ = 'minmax_offices'

    office_id = Column(String, primary_key=True, comment='地址碼')
    office_name = Column(String, nullable=False, unique=True, comment='地點名稱')
    address = Column(String, nullable=False, unique=True, comment='地址')

    # 建立到 Request 的關聯
    requests = relationship("Request", back_populates="minmax_offices")