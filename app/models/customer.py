from app import db
from app.models.rental import Rental
import datetime

class Customer(db.Model):
    #__tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String) 
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
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

    # def get_number_of_videos_checked_out(self):
    #     number_customer_has_out = Customer.query.join(Rental, self.id == Rental.customer_id, is_checked_in = False).count()
    #     return number_customer_has_out


