from app.models.base import db
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

class 專案(db.Model):
    __tablename__ = '專案'

    默認主鍵 = Column(Integer, primary_key=True, autoincrement=True)
    專案名稱 = Column(String, nullable=False, unique=True)
    啟動年份 = Column(String)
    負責人工號簡碼 = Column(String, ForeignKey('員工.工號簡碼'))
    備註 = Column(Text)
    專案狀態 = Column(String, nullable=False, server_default= '進行中') # 進行中/結案維護/廢棄
    狀態更新時間戳 = Column(DateTime(timezone=True))

    創建時間戳 = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    更新時間戳 = Column(DateTime(timezone=True), onupdate=func.now())
    刪除時間戳 = Column(DateTime(timezone=True))

    # 建立到 請購明細 的關聯
    請購明細 = relationship("請購明細", back_populates="專案", primaryjoin="請購明細.專案名稱 == 專案.專案名稱", foreign_keys="[請購明細.專案名稱]")