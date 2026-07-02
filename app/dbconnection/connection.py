from datetime import datetime

from sqlalchemy.ext.declarative import declartive_base

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declartive_base


#DB connection <motor>://<user>:<password>@<host>:<port>/<database>
engine = create_engine('postgresql://postgres:Admin123@localhost:5432/postgres')
Base = declartive_base()

class transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False) #Expense or income
    category_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    transaction_date = Column(DateTime(), default=datetime.now(), nullable=False)

    __str__ = lambda self: f"{self.description}: {self.amount}, {self.type}, {self.transaction_date}"

