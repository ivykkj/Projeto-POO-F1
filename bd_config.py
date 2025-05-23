from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from abc import ABCMeta

class DeclarativeABCMeta(DeclarativeMeta, ABCMeta):
    pass

Base = declarative_base(metaclass=DeclarativeABCMeta)
engine = create_engine('sqlite:///f1.db', echo=True)
SessionLocal = sessionmaker(bind=engine)
