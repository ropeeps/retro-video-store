from app import db
import datetime

class Video(db.Model):
    #__tablename__ = "video" #this line would override the class name, if you wanted the table name to be plural since class names are usually 
    #singular 
    id = db.Column(db.Integer, primary_key=True) #autoincrement is default for primary keys
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.today())
    total_inventory = db.Column(db.Integer)
    customers = db.relationship("Customer", secondary="rental")

    def get_video_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory
        }

