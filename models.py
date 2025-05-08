import json
from datetime import datetime, timedelta


# Transactions
class Transaction:
    def __init__(self, amount, t_type, category, timestamp, note=""):
        
        self.amount = float(amount)
        self.t_type = t_type
        self.category = category
        self.timestamp = timestamp  
        self.note = note

    # Converts the transaction to dictionary for saving to JSON
    def to_dict(self):
        return {
            "amount": self.amount,
            "t_type": self.t_type,
            "category": self.category,
            "timestamp": self.timestamp,
            "note": self.note
        }

    # returns readable date (for table display)
    def formatted_date(self):
        dt = datetime.fromisoformat(self.timestamp)
        return dt.strftime("%Y-%m-%d %H:%M")

    # returns True if it's income
    def is_income(self):
        return self.t_type.lower() == "income"
    
    
TRANSACTIONS_FILE = "data/transactions.json"


def load_transaction():
    try:
        with open(TRANSACTIONS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Convert dicts to Transaction objects
            return [
                Transaction(
                    item["amount"],
                    item["t_type"],
                    item["category"],
                    item["timestamp"],
                    item.get("note", "")  # default to empty string if "note" is missing
                )
                for item in data
            ]
    except:
        return []


# Save list of Transaction objects to the JSON file.
def save_transaction(transactions):
    with open(TRANSACTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump([t.to_dict() for t in transactions], f, indent=4)
        

# Create and save new transaction
def add_transaction(amount, t_type, category, note=""):
    timestamp = datetime.now().isoformat()
    new_transaction = Transaction(amount=amount,
        t_type=t_type,
        category=category,
        timestamp=timestamp,
        note=note
    )
    
    transactions = load_transaction()
    transactions.append(new_transaction)
    save_transaction(transactions)
    
    
# Calculate Total income/expense, and balance
def get_summary():
    transactions = load_transaction()
    
    total_income = 0
    total_expense = 0
    
    for t in transactions:
        if t.is_income():
            total_income += t.amount
        else:
            total_expense += t.amount

    balance = total_income - total_expense

    return {
        "income": total_income,
        "expense": total_expense,
        "balance": balance
    }
    

# Recent transactions
def recent_transactions(limit=10):
    transactions = load_transaction()
    
    # sort by timestamp
    for i in range(len(transactions)):
        for j in range(i + 1, len(transactions)):
            if transactions[i].timestamp < transactions[j].timestamp:
                # swap if j is more recent than i
                transactions[i], transactions[j] = transactions[j], transactions[i]
                
    recent = []
    count = 0
    for t in transactions:
        if count >= limit:
            break
        recent.append(t)
        count += 1
    
    return recent



# Filter transaction
def filter_transactions_by_date(transactions, filter_type):
    now = datetime.now()
    
    if filter_type == "day":
        cutoff = now - timedelta(days=1)
    elif filter_type == "week":
        cutoff = now - timedelta(weeks=1)
    elif filter_type == "month":
        cutoff = now - timedelta(days=30)
    elif filter_type == "year":
        cutoff = now - timedelta(days=365)
    elif filter_type == "all-time":
        return transactions
    else:
        # Default fallback (week)
        cutoff = now - timedelta(weeks=1)
    
    filtered = []
    for t in transactions:
        t_date = datetime.fromisoformat(t.timestamp)
        if t_date >= cutoff:
            filtered.append(t)
    return filtered


def render_grouped_transactions(transactions, t_type_filter, filter_type):
    # Filter by type (expense or income)
    filtered_type = [t for t in transactions if t.t_type.lower() == t_type_filter.lower()]
    
    # Filter by date range
    filtered = filter_transactions_by_date(filtered_type, filter_type)
    
    # Group by category
    category_dict = {}
    for t in filtered:
        category_dict.setdefault(t.category, []).append(t)
    
    # Build HTML rows with collapsible details
    html_rows = ""
    for idx, (category, txns) in enumerate(category_dict.items()):
        total = sum(t.amount for t in txns)
        html_rows += f"""
        <tr class="collapsible" id="{t_type_filter}-row-{idx}">
            <td>{category}</td>
            <td>${total:.2f}</td>
        </tr>
        <tr class="content" id="{t_type_filter}-content-row-{idx}" style="display:none;">
            <td colspan="2">
                <table class="inner-table">
                    <thead>
                        <tr>
                            <th>Amount</th>
                            <th>Date</th>
                            <th>Note</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        for t in txns:
            html_rows += f"""
                        <tr>
                            <td>${t.amount:.2f}</td>
                            <td>{t.formatted_date()}</td>
                            <td>{t.note}</td>
                        </tr>
            """
        html_rows += """
                    </tbody>
                </table>
            </td>
        </tr>
        """
    return html_rows
