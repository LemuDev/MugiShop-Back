from src.config.db import db

# Categories Model
class Categories(db.Model):

    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(60), unique=True)
    
    
    categories_rel = db.relationship("Products", backref="categories_rel")
