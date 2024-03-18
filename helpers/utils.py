import os
import sys
import pytz
import ntplib
import platform
import traceback
import ctypes
import pandas as pd
from pathlib import Path
from ctypes import wintypes
from typing import List, Dict, Any, Tuple, Literal
from time import ctime
from datetime import datetime
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from decimal import Decimal, ROUND_HALF_UP, ROUND_DOWN

class utils:
    @classmethod
    def make_db_connector(cls, host: str, port: str, database_name: str, username: str, password: str) -> Engine:        
        # 建立資料庫連接字串
        db_url = f'postgresql://{username}:{password}@{host}:{port}/{database_name}'

        # 建立資料庫引擎
        engine = create_engine(db_url)
        # 返回資料庫連接
        return engine