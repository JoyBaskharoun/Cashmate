from models.storage import load_transaction
from datetime import datetime
def get_summary(email):
    transactions = load_transaction()
    user_transactions = [t for t in transactions if t.email == email]
    income = sum(t.amount for t in user_transactions if t.is_income())
    expense = sum(t.amount for t in user_transactions if not t.is_income())
    return {
        "income": income,
        "expense": expense,
        "balance": income - expense
    }

def recent_transactions(email, limit=7):
    transactions = load_transaction()
    user_transactions = [t for t in transactions if t.email == email]
    
    # Create a list of tuples (transaction, parsed_datetime)
    transactions_with_dt = []
    for t in user_transactions:
        try:
            dt = datetime.fromisoformat(t.timestamp)
        except Exception:
            dt = datetime.min  # or handle differently
        transactions_with_dt.append((t, dt))

    # Sort by datetime
    transactions_with_dt.sort(key=lambda x: x[1], reverse=True)

    # Extract sorted transactions
    sorted_transactions = [t[0] for t in transactions_with_dt]
        
    return sorted_transactions[:limit]
