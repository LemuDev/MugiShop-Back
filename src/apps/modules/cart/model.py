from src.config.db import db

# Cart Model
class Cart(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    cart_items = db.relationship('CartItems', backref='cart')
    
# Cart Items Model
class CartItems(db.Model):
    
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)    
    product_id = db.Column(db.Integer(), db.ForeignKey('products.id'))
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
    is_sell = db.Column(db.Boolean(), default=False)
        
