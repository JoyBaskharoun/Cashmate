from models.storage import load_transaction
from datetime import datetime

def get_summary(email):
    transactions = load_transaction() 

    user_transactions = []
    for t in transactions:
        if t.email == email:  # only user's transactions
            user_transactions.append(t)

    income = 0
    for t in user_transactions:
        if t.is_income():
            income += t.amount 

    expense = 0
    for t in user_transactions:
        if not t.is_income():
            expense += t.amount 

    balance = income - expense  # calculate balance

    return {
        "income": income,
        "expense": expense,
        "balance": balance
    }


def recent_transactions(email, limit=7):
    transactions = load_transaction() 

    user_transactions = []
    for t in transactions:
        if t.email == email:  # filter by email
            user_transactions.append(t)

    transactions_with_dt = []
    for t in user_transactions:
        dt = datetime.fromisoformat(t.timestamp)  # convert timestamp to datetime
        transactions_with_dt.append((t, dt))

    n = len(transactions_with_dt)
    for i in range(n):
        for j in range(0, n - i - 1):
            if transactions_with_dt[j][1] < transactions_with_dt[j + 1][1]:
                # swap if older date
                transactions_with_dt[j], transactions_with_dt[j + 1] = transactions_with_dt[j + 1], transactions_with_dt[j]

    sorted_transactions = []
    for pair in transactions_with_dt:
        sorted_transactions.append(pair[0])  # get transactions only

    result = []
    count = 0
    for t in sorted_transactions:
        if count >= limit:
            break
        result.append(t)  # add to result until limit
        count += 1

    return result
