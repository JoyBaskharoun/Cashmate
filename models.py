from datetime import datetime

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
