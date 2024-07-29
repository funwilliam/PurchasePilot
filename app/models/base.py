import uuid
from datetime import datetime
from sqlalchemy import Date, DateTime, Boolean, Integer, Float, Uuid
from sqlalchemy.engine import Engine
from sqlalchemy.event import listens_for
from sqlalchemy.inspection import inspect
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True  # 這是抽象類，不會被映射到db

    def new(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def update(self):
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def to_dict(self):
        columns = inspect(self.__class__).columns
        data = {}
        for column in columns:
            attr = getattr(self, column.name)
            # 如果是 DateTime 型別，需要轉換為 ISO 格式的str
            if isinstance(column.type, DateTime):
                data[column.name] = attr.isoformat(timespec='seconds') if attr else None
            elif isinstance(column.type, Date):
                data[column.name] = attr.isoformat() if attr else None
            else:
                data[column.name] = attr
        return data
    
    @classmethod
    def from_dict(cls, data):
        columns = inspect(cls).columns
        obj = cls()
        for column in columns:
            if column.name in data:
                value = data[column.name]
                if isinstance(column.type, DateTime):
                    value = datetime.fromisoformat(value)
                elif isinstance(column.type, Date):
                    value = datetime.fromisoformat(value)
                elif isinstance(column.type, Float):
                    value = float(value)
                elif isinstance(column.type, Integer):
                    value = int(value)
                elif isinstance(column.type, Boolean):
                    if(isinstance(value, str)):
                        value = value.lower()
                        if value == 'true':
                            value = True
                        elif value == 'false':
                            value = False
                    else:
                        value = bool(value)
                elif isinstance(column.type, Uuid):
                    if value:
                        value = uuid.UUID(value)
                    else:
                        value = None
                setattr(obj, column.name, value)
        return obj

# 將 BaseModel 作為基礎模型類
db.Model = BaseModel

# sqlite資料庫啟用外鍵限制
# @listens_for(Engine, "connect")
# def set_sqlite_pragma(dbapi_connection, connection_record):
#     cursor = dbapi_connection.cursor()
#     cursor.execute("PRAGMA foreign_keys=ON")
#     cursor.close()