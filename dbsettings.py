from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

HOST = 'localhost'
PORT = 5000
USER = 'creator'
PASSWD = 123
DB_NAME = 'dataox'
DB_URL = f'postgresql://{USER}:{PASSWD}@{HOST}:{PORT}/{DB_NAME}'

engine = create_engine(DB_URL)
Base = declarative_base()

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = Session()