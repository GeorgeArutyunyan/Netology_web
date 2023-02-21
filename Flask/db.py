import atexit
from sqlalchemy import Column, String, Integer, DateTime, create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DSN = 'postgresql://app:1111@127.0.0.1:5431/netology'

engine = create_engine(DSN)

Base = declarative_base()
Session = sessionmaker(bine=engine)

atexit.register(engine.dispose)


class Shop(Base):
    __tablename__ = 'app_shop'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    text = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())


Base.metadata.drop_all(engine)
Base.metadata.create_all(bind=engine)
