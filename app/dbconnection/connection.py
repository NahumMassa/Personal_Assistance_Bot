from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import sessionmaker, declarative_base 
from sqlalchemy import create_engine

#DB connection <motor>://<user>:<password>@<host>:<port>/<database>

#connection pool
engine = create_engine('postgresql://postgres:postgres@localhost:5432/personal_finance') 


Base = declarative_base() #to create models, with the heritage of Base class
Session = sessionmaker(engine) #a session is a workspace for the db
session = Session()

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False) #Expense or income
    category_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    transaction_date = Column(DateTime(), default=datetime.now(), nullable=False)

    __str__ = lambda self: f"Description: {self.description}, Amount: {self.amount}, Type: {self.type}, Date: {self.transaction_date}"

if __name__ == "__main__":
    print('Testing DB connection')
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    