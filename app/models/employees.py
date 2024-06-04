from app.models.base import Base, db
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

class 員工(db.Model):
    __tablename__ = '員工'

    默認主鍵 = Column(Integer, primary_key=True, autoincrement=True)
    工號簡碼 = Column(String, nullable=False, unique=True)
    工號全碼 = Column(String, nullable=False, unique=True)
    姓名 = Column(String, nullable=False)
    信箱 = Column(String, nullable=False, unique=True)
    員工卡號 = Column(String, unique=True)

    創建時間戳 = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    更新時間戳 = Column(DateTime(timezone=True), onupdate=func.now())
    刪除時間戳 = Column(DateTime(timezone=True))

    # 建立到 請購紀錄明細 的關聯
    請購紀錄明細 = relationship("請購紀錄明細", back_populates="申請人")