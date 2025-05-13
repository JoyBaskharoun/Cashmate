from models.storage import load_transaction

def get_summary(username):
    transactions = load_transaction()
    user_transactions = [t for t in transactions if t.username == username]
    income = sum(t.amount for t in user_transactions if t.is_income())
    expense = sum(t.amount for t in user_transactions if not t.is_income())
    return {
        "income": income,
        "expense": expense,
        "balance": income - expense
    }

def recent_transactions(username, limit=7):
    transactions = load_transaction()
    user_transactions = [t for t in transactions if t.username == username]
    sorted_transactions = sorted(user_transactions, key=lambda t: t.timestamp, reverse=True)
    return sorted_transactions[:limit]
