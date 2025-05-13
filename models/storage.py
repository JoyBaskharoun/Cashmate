import json
from datetime import datetime
from models.transactions import Transaction

TRANSACTIONS_FILE = "data/transactions.json"

def load_transaction():
    try:
        with open(TRANSACTIONS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            transactions = []
            for username, items in data.items():
                for item in items:
                    transactions.append(Transaction(
                        username,
                        item["amount"],
                        item["t_type"],
                        item["category"],
                        item["timestamp"],
                        item.get("note", "")
                    ))
            return transactions
    except:
        return []

def save_transaction(transactions):
    grouped = {}
    for t in transactions:
        grouped.setdefault(t.username, []).append(t.to_dict())
    with open(TRANSACTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(grouped, f, indent=4)

def add_transaction(username, amount, t_type, category, note=""):
    timestamp = datetime.now().isoformat()
    new_transaction = Transaction(username, amount, t_type, category, timestamp, note)
    transactions = load_transaction()
    transactions.append(new_transaction)
    save_transaction(transactions)
