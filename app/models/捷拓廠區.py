from app.models.base import db
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.orm import relationship

class 捷拓廠區(db.Model):
    __tablename__ = '捷拓廠區'

    廠區名稱 = Column(String, primary_key=True)
    地址碼 = Column(String, nullable=False, unique=True)
    地址 = Column(String)

    創建時間戳 = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    更新時間戳 = Column(DateTime(timezone=True), onupdate=func.now())
    刪除時間戳 = Column(DateTime(timezone=True))

    # 建立到 請購明細 的關聯
    請購明細 = relationship("請購明細", back_populates="捷拓廠區", primaryjoin="請購明細.收貨廠區 == 捷拓廠區.廠區名稱", foreign_keys="[請購明細.收貨廠區]")