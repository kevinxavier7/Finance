from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Boolean, DateTime, BigInteger


class BaseUser(DeclarativeBase):
    pass

    
class User(BaseUser):
    __tablename__ = 'users'

    user_id = Column(Integer(), primary_key=True)
    document = Column(BigInteger(), unique=True, nullable=False)
    username = Column(String(50), nullable=False )
    email = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    last_name = Column(String(100))
    age = Column(BigInteger(), nullable=False)
    phone = Column(String(10), nullable=False)
    active = Column(Boolean(), default=True)
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=True)


