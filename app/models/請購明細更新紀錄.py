from app.models.base import db
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey, func
from sqlalchemy.orm import relationship

class 請購明細更新紀錄(db.Model):
    __tablename__ = '請購明細更新紀錄'
    
    默認主鍵 = Column(Integer, primary_key=True, autoincrement=True)
    請購明細主鍵 = Column(Integer, ForeignKey('請購明細.默認主鍵'), nullable=False)
    修改人工號簡碼 = Column(String)
    更新種類 = Column(String, nullable=False) # 創建 / 更新
    更新說明 = Column(Text)
    原資料 = Column(JSON)
    新資料 = Column(JSON)

    創建時間戳 = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
