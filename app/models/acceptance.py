from app.models.base import Base, db
from sqlalchemy import Column, Integer, Boolean, Float, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

class Acceptance(db.Model):
    __tablename__ = 'acceptance_notes'

    id = Column(String, primary_key=True, comment='資材部收料單號')
    receive_quantity = Column(Float, nullable=False, comment='入庫數量')
    delivery_location_id = Column(String, ForeignKey('minmax_offices.office_id'), nullable=False, comment='收貨地址碼')
    request_id = Column(Integer,  ForeignKey('requests.id'), nullable=False, comment='工程部內申請單號')
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, comment='收到驗收單時間戳')
    status = Column(Boolean, comment='驗收狀態')
    status_updated_at = Column(DateTime(timezone=True), comment='狀態更新時間戳')

    # 建立到 Request 的關聯
    request = relationship("Request", back_populates="acceptance_notes")