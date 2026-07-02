from telegram import Update
from telegram.ext import ContextTypes



#FALTA AGREFAR LA DESCRIPCIÓN DEL GASTO
async def register_expense(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Register an expense. Usage: /expense <category> <amount>"""
    args = context.args

    if len(args) != 2:
        await update.message.reply_text(
            "⚠️ Invalid format. Use: /expense <category> <amount>\n"
            "Example: /expense food 150.00"
        )
        return

    category = args[0].lower()

    try:
        amount = float(args[1])
        if amount <= 0:
            raise ValueError
        amount = -amount
    except ValueError:
        await update.message.reply_text("⚠️ Amount must be a positive number.")
        return

    # TODO: call your backend logic here, e.g.:
    # success = db.insert_expense(category, amount)

    await update.message.reply_text(
        f"✅ Expense registered!\n"
        f"📂 Category: {category}\n"
        f"💸 Amount: {amount:.2f}"
    )


async def register_income(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Register an income. Usage: /income <category> <amount>"""
    args = context.args

    if len(args) != 2:
        await update.message.reply_text(
            "⚠️ Invalid format. Use: /income <category> <amount>\n"
            "Example: /income salary 1000.00"
        )
        return

    category = args[0].lower()

    try:
        amount = float(args[1])
        if amount <= 0:
            raise ValueError
    except ValueError:
        await update.message.reply_text("⚠️ Amount must be a positive number.")
        return

    # TODO: call your backend logic here, e.g.:
    # success = db.insert_expense(category, amount)

    await update.message.reply_text(
        f"✅ Income registered!\n"
        f"📂 Category: {category}\n"
        f"💸 Amount: {amount:.2f}"
    )
