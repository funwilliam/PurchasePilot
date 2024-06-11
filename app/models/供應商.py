from app.models.base import Base, db
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.orm import relationship

class 供應商(db.Model):
    __tablename__ = '供應商'

    供應商編號 = Column(String, primary_key=True)
    簡稱 = Column(String, nullable=False, unique=True)
    全名 = Column(String, nullable=False, unique=True)
    營業項目 = Column(String)

    創建時間戳 = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    更新時間戳 = Column(DateTime(timezone=True), onupdate=func.now())
    刪除時間戳 = Column(DateTime(timezone=True))

    # 建立到 物料 的關聯
    物料 = relationship("物料", back_populates="供應商")