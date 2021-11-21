from app import db
import datetime

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True) #autoincrement is default for primary keys
    name = db.Column(db.String)
    postal_code = db.Column(db.String) 
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.today())
    videos = db.relationship("Video", secondary="rental") #secondary name should match the join table model name if you're
    #not overriding with '__tablename__'
   
    def get_cust_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "registered_at": self.registered_at
        }
