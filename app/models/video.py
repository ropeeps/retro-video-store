from app import db
from app.models.rental import Rental
import datetime

class Video(db.Model):
    #__tablename__ = "video" #this line would override the class name, if you wanted the table name to be plural since class names are usually 
    #singular 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    total_inventory = db.Column(db.Integer)
    customers = db.relationship("Customer", secondary="rental")

    def get_video_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory
        }

    # def update_inventory(self):
    #     checked_out_videos = Video.query.join(Rental, self.id == Rental.video_id, is_checked_in = False).count()
    #     available_inventory = self.total_inventory - checked_out_videos
    #     return available_inventory 

