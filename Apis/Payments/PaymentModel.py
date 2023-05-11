from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, BigInteger, Date
from Apis.Credits.CreditModel import Credit
from Apis.Users.UserModel import User


class BasePayment(DeclarativeBase):
    pass


class Payment(BasePayment):
    __tablename__ = 'payments'

    payment_id = Column(Integer(), primary_key=True)
    credit_id = Column(ForeignKey(Credit.credit_id))
    payment_value = Column(Float())
    payment_date = Column(DateTime(), nullable=False)
    user_creates = Column(ForeignKey(User.user_id))


