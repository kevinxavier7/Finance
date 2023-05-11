from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Boolean, DateTime, BigInteger, ForeignKey
from Apis.Users.UserModel import User

class BaseClient(DeclarativeBase):
    pass


class City(BaseClient):
    __tablename__ = 'city'
    
    id = Column(Integer(), primary_key=True)
    cod_city = Column(Integer(), unique=True)
    name = Column(String(100), nullable=False)
    
       
class Client(BaseClient):
    __tablename__ = 'client'

    client_id = Column(Integer(), primary_key=True)
    document = Column(BigInteger(), unique=True, nullable=False)    
    email = Column(String(100), nullable=False)    
    name = Column(String(100), nullable=False)
    last_name = Column(String(100))
    phone = Column(String(10), nullable=False)
    active = Column(Boolean(), default=True)
    address = Column(String(200),nullable=False)
    city = Column(ForeignKey("city.id"))
    profession = Column(String(100), nullable=False)
    image = Column(String(100))
    active = Column(Boolean(), default=True)
    user_creates = Column(ForeignKey(User.user_id))			
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=True)

