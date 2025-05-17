from models.storage import load_transaction
from datetime import datetime

def get_summary(email):
    transactions = load_transaction()
    
    user_transactions = []
    for t in transactions:
        if t.email == email:
            user_transactions.append(t)
    
    #total income
    income = 0
    for t in user_transactions:
        if t.is_income():
            income += t.amount
    
    #total expense
    expense = 0
    for t in user_transactions:
        if not t.is_income():
            expense += t.amount
    
    #balance
    balance = income - expense
    
    return {
        "income": income,
        "expense": expense,
        "balance": balance
    }



def recent_transactions(email, limit=7):
    transactions = load_transaction()
    
    user_transactions = []
    for t in transactions:
        if t.email == email:
            user_transactions.append(t)
    
    # Create a list of tuples (transaction, datetime)
    transactions_with_dt = []
    for t in user_transactions:
        dt = datetime.fromisoformat(t.timestamp)
        transactions_with_dt.append((t, dt))
    
    # sort in descending order
    n = len(transactions_with_dt)
    for i in range(n):
        for j in range(0, n - i - 1):
            if transactions_with_dt[j][1] < transactions_with_dt[j + 1][1]:
                # swap if the current date is older than the next
                transactions_with_dt[j], transactions_with_dt[j + 1] = transactions_with_dt[j + 1], transactions_with_dt[j]
    
    # Extract sorted transactions
    sorted_transactions = []
    for pair in transactions_with_dt:
        sorted_transactions.append(pair[0])
    
    result = []
    count = 0
    for t in sorted_transactions:
        if count >= limit:
            break
        result.append(t)
        count += 1
    
    return result
