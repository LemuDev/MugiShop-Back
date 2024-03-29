from src.config.db import db

# User Model
class Users(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    
    cart = db.relationship('Cart', backref='Users')
