from app.models.base import Base, db
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

class Material(db.Model):
    __tablename__ = 'materials'
    
    id = Column(Integer, primary_key=True, comment='默認遞增主鍵')
    material_id = Column(String, nullable=False, comment='物料代號')
    material_name = Column(String, nullable=False, comment='品名規格')
    default_material_category = Column(String, ForeignKey('material_categories.category'), nullable=False, comment='預設物料類別') # 請購單有實際物料類別欄。
    supplier_name = Column(String, ForeignKey('suppliers.short_name'), comment='供應商簡稱')
    unit_price = Column(Float, nullable=False, comment='單價')
    unit = Column(String, ForeignKey('units.unit_name'), nullable=False, comment='單位') # 外鍵確保單位統一
    currency = Column(String, ForeignKey('currencies.currency_name'), nullable=False, comment='幣別') # 外鍵確保幣別統一
    default_delivery_location_id = Column(String, ForeignKey('minmax_offices.office_id'), nullable=False, comment='預設收貨地址碼') # 資材部建檔與物料管理用，未來可能棄用。請購單有實際收貨地址欄。
    last_use_at = Column(DateTime(timezone=True), comment='最後使用時間戳')
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, comment='建檔時間戳')
    deleted_at = Column(DateTime(timezone=True), comment='廢棄時間戳')
    
    # 建立到 Supplier 的關聯
    supplier = relationship("Supplier", back_populates="materials")
