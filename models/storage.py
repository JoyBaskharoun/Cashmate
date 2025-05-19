import json
from datetime import datetime
from models.transactions import Transaction

t_file = "data/transactions.json"

def load_transaction():
    try:
        f = open(t_file, "r")
        data = json.load(f)
        f.close()
        transactions = []
        for email in data:
            items = data[email]
            for item in items:
                transactions.append(Transaction(
                    email,
                    amount=item["amount"],
                    t_type=item["t_type"],
                    category=item["category"],
                    timestamp=item["timestamp"],
                    note=item.get("note", ""),
                    id=item.get("id")
                ))
        return transactions
    except:
        return []

def save_transaction(transactions):
    grouped = {}
    for t in transactions:
        if t.email not in grouped:
            grouped[t.email] = []
        grouped[t.email].append(t.to_dict())
    f = open(t_file, "w")
    json.dump(grouped, f)
    f.close()

def add_transaction(email, amount, t_type, category, note="", timestamp=None):
    if not timestamp:
        timestamp = datetime.now().isoformat(timespec='minutes')
    new_transaction = Transaction(email, amount, t_type, category, timestamp, note)
    transactions = load_transaction()
    transactions.append(new_transaction)
    save_transaction(transactions)