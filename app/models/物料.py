from app.models.base import db
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Uuid, func
from sqlalchemy.orm import relationship

class 物料(db.Model):
    __tablename__ = '物料'
    
    默認主鍵 = Column(Integer, primary_key=True, autoincrement=True)
    供應商簡稱 = Column(String, ForeignKey('供應商.簡稱'), nullable=False) # 替代鍵_群組1
    物料代號 = Column(String, nullable=False) # 替代鍵_群組1
    品名規格 = Column(String)
    單價 = Column(Float)
    幣別 = Column(String)
    單位 = Column(String)
    預設物料類別 = Column(String) # 請購單有實際物料類別欄。
    預設收貨廠區 = Column(String) # 請購單有實際收貨地址欄。資材部建檔與物料管理用，未來可能棄用。
    
    報價單檔案主鍵 = Column(Uuid, ForeignKey('檔案.默認主鍵', ondelete='SET NULL'))

    狀態 = Column(String, server_default='正常使用', nullable=False) # 正常使用 / 尚未建檔 / 等待核准 / 報價單過期

    創建時間戳 = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    更新時間戳 = Column(DateTime(timezone=True), onupdate=func.now())
    刪除時間戳 = Column(DateTime(timezone=True))
    
    # 建立到 {請購明細, 供應商, 報價單} 的關聯
    請購明細 = relationship("請購明細", back_populates="物料", primaryjoin="and_(請購明細.供應商簡稱 == 物料.供應商簡稱, 請購明細.物料代號 == 物料.物料代號)", foreign_keys="[請購明細.供應商簡稱, 請購明細.物料代號]")
    供應商 = relationship("供應商", back_populates="物料")
    報價單 = relationship("檔案", foreign_keys='物料.報價單檔案主鍵')
    