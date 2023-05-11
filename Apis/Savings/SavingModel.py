from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from Apis.Clients.ClientModel import Client, City
from Apis.Users.UserModel import User

class BaseSaving(DeclarativeBase):
    pass


class Country(BaseSaving):
    __tablename__ = 'country'
    
    id = Column(Integer(), primary_key=True)
    cod_country = Column(Integer(), unique=True)
    name = Column(String(100), nullable=False)


class Saving(BaseSaving):
    __tablename__ = 'savings_account'
    
    account_id = Column(Integer(), primary_key=True)
    client_id = Column(ForeignKey(Client.client_id))
    account_number = Column(String(50), nullable=False, unique=True)
    balance = Column(Float())
    activation_date = Column(DateTime(), nullable=False)
    city_id = Column(ForeignKey(City.id))
    country_id = Column(ForeignKey("country.id"))
    account_status = Column(Boolean(), default=True)
    user_creates = Column(ForeignKey(User.user_id))
		
    
    
       
