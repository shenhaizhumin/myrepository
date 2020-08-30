from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from application.settings import mall_db

# db_url = conf.get('db.url', 'pg_url')
uri = f"mysql+pymysql://{mall_db['user']}:{mall_db['password']}@{mall_db['host']}:{mall_db['port']}/{mall_db['database']}"
engine = create_engine(uri, echo=True)
metadata = MetaData(bind=engine)
Base = declarative_base(bind=engine)
# 建表
# Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


def get_db_session():
    return session


def get_db():
    try:
        yield session
    finally:
        session.close()
