from app import db
from datetime import datetime

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    postal_code = db.Column(db.String) #To account for 0s; all expected outputs had strings
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime, nullable=True)

    def get_cust_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "registered_at": self.registered_at
        }


