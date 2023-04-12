
from sqlalchemy import create_engine,MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

class BaseConfig():
    DB_HOST  = os.environ.get('DB_HOST','192.168.222.163')
    DB_PORT = os.environ.get('DB_PORT','5432')
    DB_USER = os.environ.get('DB_USER','postgres')
    DB_PASSWORD = os.environ.get('DB_PASSWORD','postgres')
    DB_NAME = os.environ.get('DB_NAME','postgres')
    
# DB_URL = 'sqlite:///fastapidb.sqlite3'
conf = BaseConfig()

DB_URL = f'postgresql://{conf.DB_USER}:{conf.DB_PASSWORD}@{conf.DB_HOST}:{conf.DB_PORT}/{conf.DB_NAME}'
meta = MetaData()

# engine = create_engine(DB_URL,connect_args={'check_same_thread': False})
engine = create_engine(DB_URL)

sessionlocal = sessionmaker(autocommit=False, bind=engine)
Base =declarative_base()