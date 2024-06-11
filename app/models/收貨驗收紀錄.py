from app.models.base import Base, db
from sqlalchemy import Column, Integer, Boolean, Float, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

class 收貨驗收紀錄(db.Model):
    __tablename__ = '收貨驗收紀錄'

    資材部收料單號 = Column(String, primary_key=True)
    入庫數量 = Column(Float, nullable=False)
    收貨廠區 = Column(String, ForeignKey('捷拓廠區.廠區名稱'), nullable=False)
    工程部內申請單號 = Column(Integer, ForeignKey('請購紀錄明細.默認主鍵'), nullable=False)
    收到驗收單時間戳 = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    驗收狀態 = Column(Boolean)
    狀態更新時間戳 = Column(DateTime(timezone=True))

    創建時間戳 = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    更新時間戳 = Column(DateTime(timezone=True), onupdate=func.now())
    刪除時間戳 = Column(DateTime(timezone=True))

    # 建立到 請購紀錄明細 的關聯
    請購紀錄明細 = relationship("請購紀錄明細", back_populates="收貨驗收紀錄")