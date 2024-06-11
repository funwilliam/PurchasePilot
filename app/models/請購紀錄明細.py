from app.models.base import Base, db
from sqlalchemy import Column, Integer, Float, String, Text, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

class 請購紀錄明細(db.Model):
    __tablename__ = '請購紀錄明細'

    默認主鍵 = Column(Integer, primary_key=True, autoincrement=True)
    申請人工號簡碼 = Column(String, ForeignKey('員工.工號簡碼'), nullable=False)
    收貨廠區 = Column(String, ForeignKey('捷拓廠區.廠區名稱'), nullable=False)
    物料表主鍵 = Column(Integer, ForeignKey('物料.默認主鍵'), nullable=False)
    物料類別 = Column(String, ForeignKey('物料類別.類別'), nullable=False)
    需求數量 = Column(Float, nullable=False)
    請購類型 = Column(String, ForeignKey('請購類型.類型'), nullable=False)
    專案名稱 = Column(String, ForeignKey('專案.專案名稱'))
    用途說明 = Column(Text)
    備註 = Column(Text)
    需求到貨日期 = Column(Date, nullable=False)
    
    狀態 = Column(String)
    狀態更新時間戳 = Column(DateTime(timezone=True))

    資材部請購單號 = Column(String, ForeignKey('資材部請購單.單號'))

    創建時間戳 = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    更新時間戳 = Column(DateTime(timezone=True), onupdate=func.now())
    刪除時間戳 = Column(DateTime(timezone=True))

    # 建立到 { 捷拓廠區, 物料, 專案, 資材部請購單, 收貨驗收紀錄, 員工 } 的關聯
    捷拓廠區 =  relationship("捷拓廠區", back_populates="請購紀錄明細")
    物料 = relationship("物料", back_populates="請購紀錄明細")
    專案 = relationship("專案", back_populates="請購紀錄明細")
    資材部請購單 = relationship("資材部請購單", back_populates="請購紀錄明細")
    收貨驗收紀錄 = relationship("收貨驗收紀錄", back_populates="請購紀錄明細")
    申請人 = relationship("員工", back_populates="請購紀錄明細")