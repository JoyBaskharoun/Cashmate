from datetime import datetime

class Transaction:
    def __init__(self, username, amount, t_type, category, timestamp, note=""):
        self.username = username
        self.amount = float(amount)
        self.t_type = t_type
        self.category = category
        self.timestamp = timestamp
        self.note = note

    def to_dict(self):
        return {
            "username": self.username,
            "amount": self.amount,
            "t_type": self.t_type,
            "category": self.category,
            "timestamp": self.timestamp,
            "note": self.note
        }

    def formatted_date(self):
        dt = datetime.fromisoformat(self.timestamp)
        return dt.strftime("%y-%m-%d %H:%M")

    def is_income(self):
        return self.t_type.lower() == "income"
