from app import db, _update_db
import random

class User(db.Model):
    __tablename__ = "users"

    phone_number = db.Column(db.Text, primary_key=True)
    profession = db.Column(db.Text)
    business_type = db.Column(db.Text)
    location = db.Column(db.Text)
    orders = db.Column(db.Integer())
    gender = db.Column(db.Text)
    age = db.Column(db.Text)
    price_category = db.Column(db.Text)
    action = db.Column(db.Text)
    action_price = db.Column(db.Float())
    budget = db.Column(db.Float())
    site = db.Column(db.Text())
    site_url = db.Column(db.Text())

    def __init__(self, phone_number):
        self.phone_number = phone_number