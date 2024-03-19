from app.models.base import Base, db
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

class Employee(db.Model):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, comment='默認遞增主鍵')
    short_num = Column(String, nullable=False, unique=True, comment='工號簡碼')
    full_num = Column(String, nullable=False, unique=True, comment='工號全碼')
    name = Column(String, nullable=False, comment='姓名')
    email = Column(String, nullable=False, unique=True, comment='公司信箱')
    card_num = Column(String, comment='員工卡號')
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, comment='建檔時間戳')
    deleted_at = Column(DateTime(timezone=True), comment='軟刪除時間戳')

    # 建立到 Request 的關聯
    requests = relationship("Request", back_populates="employees")