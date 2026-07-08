# Here we'll deal with the logic of transactions

# We'll need to import our models
from app.models import session, Transaction, Category


def register_transaction(category_name: str, amount: float, description: str):
    """
    Registers a new transaction in the database.
    
    Args:
        category_name: The name of the category.
        amount: The amount of the transaction.
        description: The description of the transaction.
        
    Returns:
        A message indicating whether the transaction was registered successfully or not.
    """

    #validate category exists
    category = session.query(Category).where(Category.name == category_name).one_or_none()
    if category is None:
        return "Category name not found, please try again"
    try:
        new_transaction = Transaction(
            type = type,
            category_id = category.id,
            amount = amount,
            description = description
        )

        session.add(new_transaction)
        session.commit()
        return f"Transaction added successfully: {type} - {category_name} - {amount} - {description}"
        
    except Exception as e:
        session.rollback()
        return f"Error: {str(e)}"


def register_category(category_name:str, category_type: str, description: str):
    """
    Registers a new category in the database.
    
    Args:
        category_name: The name of the category.
        category_type: The type of the category.
        description: The description of the category.
        
    Returns:
        A message indicating whether the category was registered successfully or not.
    """
    if category_name is None:
        raise ValueError("Category name cannot be empty")
    
    if category_type not in ["expense", "income"]:
        raise ValueError("Category type must be expense or income")
        
    if description is None:
        description = "No description was provided"
    
    #check if category exists
    category = session.query(Category).where(Category.name == category_name).one_or_none()
    if category is not None:
        raise ValueError("Category already exists")
    
    try:
        new_category = Category(
            name = category_name,
            type = category_type,
            description = description
        )

        session.add(new_category)
        session.commit()

        return f"Category added successfully: {category_name} - {category_type} - {description}"
        
    except Exception as e:
        session.rollback()
        return f"Error: {str(e)}"

def get_all_categories()->list:
    """
    Returns a list of all categories.
    """
    return [cat[0] for cat in session.query(Category.name).all()]


if __name__ == "__main__":
    #register values 
    register_category("Test_Category", "expense", "Groceries")
    print("Category added successfully")
    
    print(register_transaction("food", -10.05, "Groceries"))

    print(get_all_categories())

    #delete added categories
    #categories = session.query(Category).where(Category.name == "Test_Category").delete()
    #session.commit()

