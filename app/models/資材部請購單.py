from app.models.base import db
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.orm import relationship

class 資材部請購單(db.Model):
    __tablename__ = '資材部請購單'

    單號 = Column(String, primary_key=True)
    請購單狀態 = Column(String)
    狀態更新時間戳 = Column(DateTime(timezone=True))

    創建時間戳 = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    刪除時間戳 = Column(DateTime(timezone=True))

    # 建立到 請購明細 的關聯
    請購明細 = relationship("請購明細", back_populates="資材部請購單")