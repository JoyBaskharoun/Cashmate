from datetime import datetime
import uuid

class Transaction:
    def __init__(self, email, amount, t_type, category, timestamp, note="", id=None):
        self.email = email
        self.amount = float(amount)
        self.t_type = t_type
        self.category = category
        self.timestamp = timestamp
        self.note = note
        self.id = id if id else str(uuid.uuid4())

    def to_dict(self):
        return {
            "email": self.email,
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
