import os
import sys
import pytz
import ctypes
import pyodbc
import ntplib
import platform
import traceback
import pandas as pd
from pathlib import Path
from ctypes import wintypes
from typing import List, Dict, Any, Tuple, Literal
from time import ctime
from datetime import datetime
from sqlalchemy.engine import Engine, URL
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from decimal import Decimal, ROUND_HALF_UP, ROUND_DOWN

class utils:
    @classmethod
    def make_postgresql_DBURL(cls, user: str, password: str, host: str, port: str, database_name: str) -> str:
        """ 建立資料庫連接字串 """
        db_url = f"postgresql://{user}:{password}@{host}:{port}/{database_name}"
        return db_url
    
    @classmethod
    def make_access_DBURL(cls, access_db_path) -> str:
        """ 建立資料庫連接字串 """
        # Name of Driver from Step 1
        connection_str = r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
        connection_str += f'DBQ={access_db_path};'

        # Create Connection
        connection_url = URL.create("access+pyodbc", query={"odbc_connect": connection_str})
        # engine = create_engine(connection_url)
        return connection_url
    
    @classmethod
    def make_sqlite_DBURL(cls, access_db_path) -> str:
        """ 建立資料庫連接字串 """
        db_url = f"sqlite:///{access_db_path}"
        return db_url