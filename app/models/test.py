# pyrefly: ignore [missing-import]
from sqlalchemy.orm import sessionmaker
from connection import engine, Transaction

Session = sessionmaker(engine)

session = Session()


#----------
# Adding a value

transaction_test1 = Transaction(
    type="Expense",
    category_id=1,
    amount=10.05,
    description="Groceries"
)

transaction_test2 = Transaction(
    type="Income",
    category_id=2,
    amount=50.50,
    description="Salary"
)

transaction_test3 = Transaction(
    type="Expense",
    category_id=3,
    amount=5.50,
    description="Coffee"
)
#add 1
#session.add(transaction_test1)
#add many
session.add_all([transaction_test2, transaction_test3])
session.commit()

#----------
# Retrieving values

#SELECT * FROM transactions
print("-" * 50)
all_transactions = session.query(Transaction).all()
for transaction in all_transactions:
    print(f"Description: {transaction.description}, Amount: {transaction.amount}, Type: {transaction.type}, Date: {transaction.transaction_date}")

#SELECT * FROM transactions WHERE id=2 
print("-" * 50)
transaction1 = session.query(Transaction).filter_by(id=2).one_or_none()
#other methods: first(), first_or_none(), all(), one()
#if results retrives more than one, it's gonna return an error
print(transaction1)
print(transaction1.id)
print(transaction1.description)
print(transaction1.amount)
print(transaction1.type)
print(transaction1.transaction_date)
print(transaction1.category_id)

#----------
# Updating Values 

transaction = session.query(Transaction).filter_by(id=1).first()
transaction.amount = 90
session.commit()

#----------
# Deleting Values 

transaction = session.query(Transaction).filter_by(id=1).first()
session.delete(transaction)
session.commit()
