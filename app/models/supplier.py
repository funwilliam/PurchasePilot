from app.models.base import Base, db
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.orm import relationship

class Supplier(db.Model):
    __tablename__ = 'suppliers'

    supplier_id = Column(String, primary_key=True, comment='供應商編號')
    short_name = Column(String, nullable=False, unique=True, comment='廠內簡稱')
    full_name = Column(String, nullable=False, unique=True, comment='公司全名')
    business_item = Column(String, nullable=True, comment='營業項目')
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, comment='建檔時間戳')

    # 建立到 Material 的關聯
    materials = relationship("Material", back_populates="supplier")