import uuid
from app.models.base import db
from sqlalchemy import Column, Boolean, String, DateTime, Uuid, func, text
from sqlalchemy.orm import relationship

class 檔案(db.Model):
    __tablename__ = '檔案'

    默認主鍵 = Column(Uuid, primary_key=True, default=uuid.uuid4)
    內容分類 = Column(String, server_default='其他文件', nullable=False) # 報價單 / 規格圖 / 計畫書 / 其他文件
    檔案說明 = Column(String)
    副檔名 = Column(String)
    檔案路徑 = Column(String)
    哈希值 = Column(String, unique=True)
    
    快取 = Column(Boolean, server_default=text('FALSE'))

    創建時間戳 = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    更新時間戳 = Column(DateTime(timezone=True), onupdate=func.now())
    刪除時間戳 = Column(DateTime(timezone=True))

    物料 = relationship('物料', back_populates='報價單', passive_deletes=True)

    # 多對多關係
    請購明細 = relationship("請購明細", secondary='請購明細附件檔案關聯表', back_populates='附件檔案')
    