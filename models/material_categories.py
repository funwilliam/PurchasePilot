from models import Base
from sqlalchemy import Column, String

class Material_Category(Base):
    __tablename__ = 'material_categories'

    category = Column(String, primary_key=True, comment='物料類別')