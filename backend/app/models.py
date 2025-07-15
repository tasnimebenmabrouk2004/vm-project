from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class VM(Base):
    __tablename__ = "vms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    os = Column(String, nullable=False)
    cpu = Column(Integer, nullable=False)
    ram = Column(Integer, nullable=False)
    status = Column(String, default="stopped")  
