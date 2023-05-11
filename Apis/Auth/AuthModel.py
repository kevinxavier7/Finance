from sqlalchemy.orm import DeclarativeBase
from Apis.Users.UserModel import User
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from datetime import datetime


class BaseAuth(DeclarativeBase):
    pass


class Module(BaseAuth):    
    __tablename__ = 'module'
    
    id = Column(Integer(), primary_key=True)
    name = Column(String(100), nullable=False)
    

class PermissionsModule(BaseAuth):    
    __tablename__ = 'permissions_module'
    
    id = Column(Integer(), primary_key=True)
    user_id = Column(ForeignKey(User.user_id))
    module_id = Column(ForeignKey('module.id'))
    active = Column(Boolean(), default= True)
    created_at = Column(DateTime(), default=datetime.now())
    updated_at = Column(DateTime(), nullable=True)
    