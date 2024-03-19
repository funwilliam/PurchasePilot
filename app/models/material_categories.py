from app.models.base import Base, db
from sqlalchemy import Column, String

class Material_Category(db.Model):
    __tablename__ = 'material_categories'

    category = Column(String, primary_key=True, comment='物料類別')