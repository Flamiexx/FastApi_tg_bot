from sqlalchemy import Column, Integer, Float, String, Date, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True, index=True)
    amount_uah = Column(Float, nullable=False)
    amount_usd = Column(Float, nullable=False)
    usd_rate = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String)
    date = Column(Date, server_default=func.current_date())
