import json
from . import db

class VisitorLog(db.Model):
    __tablename__ = "visitor_logs"

    id = db.Column(db.String(36), primary_key=True)
    visitor_name = db.Column(db.String(60), nullable=False)
    host_name = db.Column(db.String(60), nullable=False)
    purpose = db.Column(db.String(140), nullable=False)
    card_number = db.Column(db.String(4), nullable=False)
    time_in = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    time_out = db.Column(db.DateTime, nullable=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def save_data(self, data):
        self.visitor_name = data.get("visitorName")
        self.host_name = data.get("hostName")
        self.purpose = data.get("purpose")
        self.card_number = data.get("cardNumber")
        self.save()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'visitorName': self.visitor_name,
            'hostName': self.host_name,
            'purpose': self.purpose,
            'cardNumber': self.card_number,
            'timeIn': str(self.time_in),
            'timeOut': str(self.time_out)
        }
