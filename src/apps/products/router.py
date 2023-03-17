from flask import Blueprint, jsonify
from .seed_products import products as products_seed
from .models import Products
from src.config.db import db



bp = Blueprint("products", __name__, url_prefix="/api")

@bp.route("/seed-products")
def deed_products():
    
        
    for p in products_seed:
        products = Products()
        
        products.name = p["name"]
        products.price = p["price"]
        products.description = ''
        products.image = p["image"]
        products.is_sell = p["is_sell"]        
        
        db.session.add(products)
        db.session.commit()
        
        
        print(p)
        


        
                
    
    return jsonify( {} )




