import json
from datetime import datetime
from models.transactions import Transaction

t_file = "data/transactions.json"

def load_transaction():
    try:
        with open(t_file, "r") as f:
            data = json.load(f)
            transactions = []
            for email, items in data.items():
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
        grouped.setdefault(t.email, []).append(t.to_dict())
    with open(t_file, "w") as f:
        json.dump(grouped, f, indent=4)

def add_transaction(email, amount, t_type, category, note="", timestamp=None):
    if timestamp is None:
        timestamp = datetime.now().isoformat(timespec='minutes')
    new_transaction = Transaction(email, amount, t_type, category, timestamp, note)
    transactions = load_transaction()
    transactions.append(new_transaction)
    save_transaction(transactions)
