from app import db
from sqlalchemy.orm import backref
import datetime

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False) 
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    due_date = db.Column(db.DateTime, default=datetime.datetime.today() + datetime.timedelta(days=7))
    customer = db.relationship("Customer", backref=backref("rentals", cascade = "delete"))
    video = db.relationship("Video", backref=backref("rentals", cascade = "delete"))
    is_checked_in = db.Column(db.Boolean)


#pure join table = no other attributes present besides foreign key(s)
#this is not a pure join table because we also have a due_date attribute 


#for deleting, mark an attribute on an instance as 'deleted' instead of deleting the whole row. from a data/ business perspective,
#this ensures records of customers and videos don't disappear forever 
