from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# 1. User
class User(Base):
    # 1. Table Name
    __tablename__ = "users"
    # 2. Attributes
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, index=True)
    role = Column(String(32), nullable=False)
    # 3. Relationships
    license_plates = relationship("LicensePlate", back_populates="user")

class LicensePlate(Base):
    # 1. Table Name
    __tablename__ = "license_plates"
    # 2. Basic Attributes
    id = Column(Integer, primary_key=True, index=True)
    plate = Column(String(16), unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    # 3. Relationships
    user = relationship("User", back_populates="license_plates")

class Identity(Base):
    __tablename__ = "identity"
    id = Column(Integer, primary_key=True)

