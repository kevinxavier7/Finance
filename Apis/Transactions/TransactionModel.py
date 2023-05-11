from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from Apis.Savings.SavingModel import Saving
from Apis.Clients.ClientModel import Client
from Apis.Users.UserModel import User


class BaseTransaction(DeclarativeBase):
    pass


class Transaction(BaseTransaction):
    __tablename__ = 'transaction'
    
    transaction_id = Column(Integer(), primary_key=True)
    account_id = Column(ForeignKey(Saving.account_id))
    client_id = Column(ForeignKey(Client.client_id))    
    transaction_value = Column(Float())
    date_transaction = Column(DateTime())     
    transaction_status = Column(String(1), default=True)
    user_creates = Column(ForeignKey(User.user_id))	