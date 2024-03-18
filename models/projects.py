from models import Base
from sqlalchemy import Column, Integer, Boolean, String, Text, DateTime, func
from sqlalchemy.orm import relationship

class Project(Base):
    __tablename__ = 'ed_projects'

    id = Column(Integer, primary_key=True, comment='默認遞增主鍵')
    launch_year = Column(String, comment='專案啟動年份')
    project_name = Column(String, nullable=False, unique=True, comment='專案名稱')
    remarks = Column(Text, comment='備註')
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, comment='建檔時間戳')
    is_active = Column(Boolean, server_default= 'true', comment='進行中/結案')

    # 建立到 Request 的關聯
    requests = relationship("Request", back_populates="ed_projects")