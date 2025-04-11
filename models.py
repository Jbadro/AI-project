from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    preferences = db.relationship('UserPreferences', backref='user', uselist=False)

class UserPreferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    diet_type = db.Column(db.String(50))  # e.g., vegan, keto, paleo
    calorie_target = db.Column(db.Integer)
    budget = db.Column(db.Float)  # Weekly budget
    allergies = db.Column(db.String(255))  # Comma-separated list of allergies
    date_updated = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now())

class GroceryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    calories = db.Column(db.Integer)
    protein = db.Column(db.Float)
    carbs = db.Column(db.Float)
    fat = db.Column(db.Float)
    category = db.Column(db.String(50))  # e.g., fruit, vegetable, meat
    store = db.Column(db.String(100))  # Store where item is available
    date_added = db.Column(db.DateTime(timezone=True), default=func.now())
