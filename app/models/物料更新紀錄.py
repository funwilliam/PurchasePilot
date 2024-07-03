from app.models.base import db
from sqlalchemy import Column, Integer, Boolean, String, Text, DateTime, JSON, func, text
from sqlalchemy.orm import relationship

class 物料更新紀錄(db.Model):
    __tablename__ = '物料更新紀錄'
    
    默認主鍵 = Column(Integer, primary_key=True, autoincrement=True)
    申請人工號簡碼 = Column(String, nullable=False)
    更新種類 = Column(String, nullable=False) # 創建 / 更新
    供應商簡稱 = Column(String, nullable=False)
    物料代號 = Column(String, nullable=False)
    通知資材 = Column(Boolean, nullable=False, server_default=text('TRUE'))
    更新說明 = Column(Text)
    原資料 = Column(JSON)
    新資料 = Column(JSON)

    創建時間戳 = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    