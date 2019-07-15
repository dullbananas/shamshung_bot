import os
from sqlalchemy import create_engine, Column, Integer, BigInteger, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine(os.getenv('SHAMSHUNG_DB_URL'))
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Prefix(Base):
	__tablename__ = 'prefixes'
	server_id = Column(BigInteger, primary_key=True)
	prefix = Column(String(32))


Base.metadata.create_all(engine)
