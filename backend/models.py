from sqlalchemy import Column, String, Integer, Boolean, JSON
from database import Base

class User(Base):
    __tablename__ = "users"

    client_id = Column(String, primary_key=True, index=True)
    organization_id = Column(String)
    segment = Column(String)
    role = Column(String)
    organizations = Column(Integer)
    current_method = Column(String)
    mobile_app = Column(Boolean)
    available_methods = Column(JSON)
    claims = Column(Integer)

    class Config:
        from_attributes = True

class UserSignature(Base):
    __tablename__ = "user_signatures"

    client_id = Column(String, primary_key=True, index=True)
    common_mobile = Column(Integer, default=0)
    common_web = Column(Integer, default=0)
    special_mobile = Column(Integer, default=0)
    special_web = Column(Integer, default=0)
