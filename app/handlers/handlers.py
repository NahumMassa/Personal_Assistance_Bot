from telegram import Update
# pyrefly: ignore [missing-import]
from telegram.ext import ContextTypes
from app.services.transaction import register_transaction, get_all_categories, register_category


#FOR FUTURE: we can handle the transaction with 2 approaches:
#1. verify if the amount is negative or positive and based on that, expense or income
#2. have 2 functions to register each type of transaction (/expense, /income) more robust, but less user-friendly, for the moment we'll use the first approach
#now, I'll handle the first approach.

def _verify_input(category, amount, description, all_categories, mode='incomn'):
    """
    Verify if the input is valid.
    Returns True if valid, otherwise returns an error message.
    """
    
    try:    
        category = category.lower()
        amount = float(amount)
        description = description

        if mode == 'income':
            if amount < 0:
                raise ValueError("Invalid amount. Amount must be positive")

        elif mode == 'expense':
            if amount > 0:
                raise ValueError("Invalid amount. Amount must be negative")

        #check is category exists in the db 
        if category not in all_categories:
            raise ValueError(f"Invalid category '{category}'. Category not found in the db")
            
        #convert amount to float and check if it's a valid number
        if amount == 0:
            raise ValueError("Invalid amount. Amount cannot be zero")

        return (category, amount, description) #return the values for next step
        
    except ValueError as e:
        return str(e)
    
        

async def register_transaction_telegram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    register an transaction based on the amount, if the amount is negative, it's an expense, if it's positive, it's an income
    Usage: /transaction <category> <amount> <description>
    """
    #for updated messages event type
    if not update.message:
        return
    
    #get all categories from a db query
    all_categories = get_all_categories()
    args = context.args

    #INPUT VALIDATION
    try:
        #check if the number of arguments is valid
        if len(args) != 3:
            await update.message.reply_text(
                "⚠️ Invalid format. Use: /transaction <category> <amount> <description>\n"
                "Example: /transaction food 150.00 Groceries"
            )
            return

        category = args[0].lower()
        amount = float(args[1])
        description = args[2]

        #check is category exists in the db 
        if category not in all_categories:
            await update.message.reply_text(
                f"Invalid category '{category}'. Category not found in the db"
            )
            return

        #convert amount to float and check if it's a valid number
        if amount == 0:
            await update.message.reply_text("Invalid amount. Amount cannot be zero")
            return 
        
    except ValueError:
        await update.message.reply_text("Invalid amount. Amount must be a number")
        return
    
    #DB OPERATION
    try:
        message = register_transaction(category, amount, description)
        await update.message.reply_text(message)
        
    except ValueError:
        await update.message.reply_text("Invalid amount. Amount must be a number")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")   

async def register_category_telegram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    register a category
    Usage: /register_category <category_name> <category_type> <description>
    """
    args = context.args
    if len(args) != 3:
        await update.message.reply_text(
            "⚠️ Invalid format. Use: /register_category <category_name> <category_type> <description>\n"
            "Example: /register_category food expense Groceries"
        )
        return

    message = register_category(args[0], args[1], args[2])
    await update.message.reply_text(message)
    


async def register_expense_telegram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Register an expense. Usage: /expense <category> <amount> <description>
    """

    #for updated messages event type
    if not update.message:
        return

    args = context.args

    #get args
    if len(args) != 3:
        await update.message.reply_text(
            "⚠️ Invalid format. Use: /expense <category> <amount>\n"
            "Example: /expense food 150.00"
        )
        return

    all_categories = get_all_categories()
    category = args[0].lower()
    amount = float(args[1])
    description = args[2]

    
    #INPUT VALIDATION
    message = _verify_input(category, amount, description, all_categories, mode='expense')
    if isinstance(message, str):
        await update.message.reply_text(message)
        return
    
    category, amount, description = message
    
    #DB OPERATIONS
    try:
        message = register_transaction(category, amount, description)
        await update.message.reply_text(message)
        
    except ValueError:
        await update.message.reply_text("Invalid amount. Amount must be a number")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}") 
    
    #finally reply to the user 
    await update.message.reply_text(
        f"✅ Expense registered!\n"
        f"📂 Category: {category}\n"
        f"💸 Amount: {amount:.2f}"
    )

async def register_income_telegram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Register an income. Usage: /income <category> <amount> <description>
    """
    #for updated messages event type
    if not update.message:
        return
    
    args = context.args

    #get args
    if len(args) != 3:
        await update.message.reply_text(
            "⚠️ Invalid format. Use: /income <category> <amount> <description>\n"
            "Example: /income food 150.00"
        )
        return

    all_categories = get_all_categories()
    category = args[0].lower()
    amount = float(args[1])
    description = args[2]

    
    #INPUT VALIDATION
    message = _verify_input(category, amount, description, all_categories, mode='income')
    if isinstance(message, str):
        await update.message.reply_text(message)
        return
    
    category, amount, description = message
    
    #DB OPERATIONS
    try:
        message = register_transaction(category, amount, description)
        await update.message.reply_text(message)
        
    except ValueError:
        await update.message.reply_text("Invalid amount. Amount must be a number")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}") 
    
    #finally reply to the user 
    await update.message.reply_text(
        f"✅ Expense registered!\n"
        f"📂 Category: {category}\n"
        f"💸 Amount: {amount:.2f}"
    )


