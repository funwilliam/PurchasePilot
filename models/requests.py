from models import Base
from sqlalchemy import Column, Integer, Float, String, Text, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

class Request(Base):
    __tablename__ = 'requests'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='工程部內申請單號')
    applicant = Column(String, ForeignKey('employees.short_num'), nullable=False, comment='申請人工號簡碼')
    delivery_location_id = Column(String, ForeignKey('minmax_offices.office_id'), nullable=False, comment='收貨地址碼')
    material_pk = Column(Integer, ForeignKey('materials.id'), nullable=False, comment='物料表主鍵')
    material_category = Column(String, ForeignKey('material_categories.category'), nullable=False, comment='物料類別')
    demand_quantity = Column(Float, nullable=False, comment='需求數量')
    request_type = Column(String, ForeignKey('request_types.type'), nullable=False, comment='請購類型')
    project_name = Column(String, ForeignKey('ed_projects.project_name'), comment='專案名稱')
    usage_description = Column(Text, comment='用途說明')
    remarks = Column(Text, comment='備註')
    demand_date = Column(Date, nullable=False, comment='需求到貨日期')
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, comment='填單時間戳')
    deleted_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, comment='軟刪除時間戳')
    status = Column(String, comment='最新狀態')
    status_updated_at = Column(DateTime(timezone=True), comment='狀態更新時間戳')
    requisition_id = Column(String, ForeignKey('purchase_requisitions.id'), comment='資材部請購單號')

    # 建立到 Office 和 Material 和 Project 和 Requisition 和 Acceptance 和 Employee 的關聯
    office =  relationship("Office", back_populates="requests")
    material = relationship("Material", back_populates="requests")
    project = relationship("Project", back_populates="requests")
    requisition = relationship("Requisition", back_populates="requests")
    acceptance_notes = relationship("Acceptance", back_populates="requests")
    employee = relationship("Employee", back_populates="requests")