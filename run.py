import os
import dotenv
from typing import List
from sqlalchemy.orm import Session, scoped_session, sessionmaker

def generate_init_file(dir: List[str]  = []):
    for directory in dir:
        init_file_conf = []
        init_file_conf_path = os.path.join(directory, 'config.txt')
        if os.path.exists(init_file_conf_path):
            with open(init_file_conf_path, 'r') as file:
                for line in file:
                    init_file_conf.append(line.strip())
        init_file_path = os.path.join(directory, '__init__.py')
        with open(init_file_path, 'w') as file:
            print('建立文件', init_file_path)
            for filename in init_file_conf:
                file.write(f'from {filename} import *\n')
            for childlevel in os.listdir(directory):
                if childlevel != '__pycache__' and childlevel != '__init__.py' and childlevel.endswith('.py'):
                    module_path = '.' + os.path.splitext(childlevel)[0]
                    try:
                        init_file_conf.index(module_path)
                    except:
                        file.write(f'from {module_path} import *\n')
generate_init_file(['helpers', 'models'])

from helpers import utils
from models import Base

if __name__ == "__main__":
    dotenv.load_dotenv()
    connector = utils.make_db_connector(
        os.getenv('DB_HOST'),       # type: ignore
        os.getenv('DB_PORT'),       # type: ignore
        os.getenv('DB_NAME'),       # type: ignore
        os.getenv('DB_USER'),       # type: ignore
        os.getenv('DB_PASSWORD')    # type: ignore
    )
    Base.metadata.create_all(connector) # 如果資料庫缺表，將會建表
    session_factory: scoped_session[Session] = scoped_session(sessionmaker(bind = connector))
    session = session_factory()