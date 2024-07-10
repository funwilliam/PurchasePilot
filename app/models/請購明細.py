from app.models.base import db
from sqlalchemy import Column, Integer, Float, String, Text, Date, DateTime, Uuid, ForeignKey, Table, func
from sqlalchemy.orm import relationship

class 請購明細(db.Model):
    __tablename__ = '請購明細'

    默認主鍵 = Column(Integer, primary_key=True, autoincrement=True)
    供應商簡稱 = Column(String, nullable=False)
    物料代號 = Column(String, nullable=False)
    單價 = Column(Float, nullable=False)
    幣別 = Column(String, nullable=False)
    單位 = Column(String, nullable=False)
    物料類別 = Column(String, nullable=False)
    需求數量 = Column(Float, nullable=False)
    申請人工號簡碼 = Column(String, nullable=False)
    需求到貨日期 = Column(Date, nullable=False)
    收貨廠區 = Column(String, nullable=False)
    請購類型 = Column(String, nullable=False)
    專案名稱 = Column(String)
    用途說明 = Column(Text)
    備註 = Column(Text)
    
    狀態 = Column(String)
    狀態更新時間戳 = Column(DateTime(timezone=True))

    資材部請購單號 = Column(String, ForeignKey('資材部請購單.單號'))

    創建時間戳 = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    更新時間戳 = Column(DateTime(timezone=True)) # 當內容更新 / 修正時使用，排除元數據改變
    刪除時間戳 = Column(DateTime(timezone=True))

    # 建立到 { 捷拓廠區, 物料, 專案, 資材部請購單, 收貨驗收紀錄, 員工 } 的關聯
    捷拓廠區 = relationship("捷拓廠區", back_populates="請購明細", primaryjoin="請購明細.收貨廠區 == 捷拓廠區.廠區名稱", foreign_keys="[請購明細.收貨廠區]")
    物料 = relationship("物料", back_populates="請購明細", primaryjoin="and_(請購明細.供應商簡稱 == 物料.供應商簡稱, 請購明細.物料代號 == 物料.物料代號)", foreign_keys="[請購明細.供應商簡稱, 請購明細.物料代號]")
    專案 = relationship("專案", back_populates="請購明細", primaryjoin="請購明細.專案名稱 == 專案.專案名稱", foreign_keys="[請購明細.專案名稱]")
    資材部請購單 = relationship("資材部請購單", back_populates="請購明細")
    收貨驗收紀錄 = relationship("收貨驗收紀錄", back_populates="請購明細")
    申請人 = relationship("員工", back_populates="請購明細", primaryjoin="請購明細.申請人工號簡碼 == 員工.工號簡碼", foreign_keys="[請購明細.申請人工號簡碼]")
    
    # 多對多關係
    附件檔案 = relationship("檔案", secondary='Mapping_請購明細_檔案', back_populates='請購明細')

    def to_dict(self):
        data = super().to_dict()
        data['附件檔案'] = [file.to_dict() for file in self.附件檔案] if self.附件檔案 else []
        return data


# 定義關聯表
Mapping請購明細檔案 = Table(
    'Mapping_請購明細_檔案', db.metadata,
    Column('請購明細主鍵', Integer, ForeignKey('請購明細.默認主鍵', ondelete='CASCADE'), primary_key=True),
    Column('檔案主鍵', Uuid, ForeignKey('檔案.默認主鍵', ondelete='CASCADE'), primary_key=True)
)