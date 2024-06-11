from app.models.base import Base, db
from sqlalchemy import Column, Integer, Boolean, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

class 物料(db.Model):
    __tablename__ = '物料'
    
    默認主鍵 = Column(Integer, primary_key=True, autoincrement=True)
    物料代號 = Column(String, nullable=False)
    供應商簡稱 = Column(String, ForeignKey('供應商.簡稱'))
    品名規格 = Column(String, nullable=False)
    單價 = Column(Float, nullable=False)
    幣別 = Column(String, nullable=False)
    單位 = Column(String, nullable=False)
    預設收貨廠區 = Column(String, ForeignKey('捷拓廠區.廠區名稱'), nullable=False) # 資材部建檔與物料管理用，未來可能棄用。請購單有實際收貨地址欄。
    預設物料類別 = Column(String, ForeignKey('物料類別.類別')) # 請購單有實際物料類別欄。
    
    報價單路徑 = Column(String)
    報價單有效期限 = Column(DateTime(timezone=True))

    啟用信標 = Column(Boolean, server_default='true', nullable=False)

    創建時間戳 = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    更新時間戳 = Column(DateTime(timezone=True), onupdate=func.now()) # 僅用於補充資料or更正錯誤資料使用，不停用
    刪除時間戳 = Column(DateTime(timezone=True)) # 停用
    
    # 建立到 請購紀錄明細 供應商 的關聯
    請購紀錄明細 = relationship("請購紀錄明細", back_populates="物料")
    供應商 = relationship("供應商", back_populates="物料")
    