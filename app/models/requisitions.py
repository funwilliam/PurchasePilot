from app.models.base import Base, db
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship

class Requisition(db.Model):
    __tablename__ = 'purchase_requisitions'

    id = Column(String, primary_key=True, comment='資材部請購單號')
    ATD_at = Column(DateTime(timezone=True), comment='送單時間戳')
    status = Column(String, comment='請購單狀態')
    status_updated_at = Column(DateTime(timezone=True), comment='狀態更新時間戳')

    # 建立到 Request 的關聯
    requests = relationship("Request", back_populates="purchase_requisitions")