from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, BigInteger, Float
from Apis.Clients.ClientModel import Client
from Apis.Users.UserModel import User


class BaseCredit(DeclarativeBase):
    pass


class Credit(BaseCredit):
    __tablename__ = 'credit'

    credit_id = Column(Integer(), primary_key=True)
    client_id = Column(ForeignKey(Client.client_id))
    credit_value = Column(Float(), nullable=False)
    installments = Column(Float(), nullable=False)
    term = Column(BigInteger(), nullable=False)
    date_credit = Column(DateTime(), nullable=False)
    payment_date = Column(BigInteger(), nullable=False)
    user_creates = Column(ForeignKey(User.user_id))


class CreditDetail(BaseCredit):
    __tablename__ = 'credit_detail'

    id = Column(Integer(), primary_key=True)
    credit_id = Column(ForeignKey('credit.credit_id'))
    installments_paid = Column(BigInteger(), nullable=False)
    next_payment_date = Column(DateTime(), nullable=False)
    last_payment_date = Column(DateTime(), nullable=True)
    credit_status = Column(String(1))
    balance = Column(Float(), nullable=False)
    user_creates = Column(ForeignKey(User.user_id))
