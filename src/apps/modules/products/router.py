from flask import Blueprint
from flask import request, jsonify
from src.config.db import db
from src.apps.modules.categories.model import Categories

from .seed_categories import categories as categories_seed
from .seed_products import products as products_seed

from .model import Products
from .schemas import ProductsSchemas

bp = Blueprint("products", __name__, url_prefix="/api")



# End Point for see all products
@bp.route("/products", methods=["GET"])
def products_list():
    products_schema = ProductsSchemas(many=True)
    
    name = request.args.get("name")
    category = request.args.get("category")

    if name is not None:
        products_by_name = Products.query.filter(Products.name.ilike("%" + name + "%")).filter_by(is_sell=False).all()
        products_by_name_count = Products.query.filter(Products.name.ilike("%" + name + "%")).filter_by(is_sell=False).count()
        
        if category is not None:
            products_by_name = Products.query.filter(Products.name.ilike("%" + name + "%")).filter_by(categories=category).filter_by(is_sell=False).all()
            products_by_name_count = Products.query.filter(Products.name.ilike("%" + name + "%")).filter_by(categories=category).filter_by(is_sell=False).count()
        
        if products_by_name_count  >= 1:
      
            for p in products_by_name:
                p.categories = p.categories_rel.name
                
        return jsonify( products_schema.dump(products_by_name) )
    else:
        if category is not None:
            products_by_name = Products.query.filter_by(categories=category).filter_by(is_sell=False).all()
            products_by_name_count = Products.query.filter_by(categories=category).filter_by(is_sell=False).count()
        
        
            if products_by_name_count  >= 1:

                for p in products_by_name:
                    p.categories = p.categories_rel.name        
            
            return jsonify( products_schema.dump(products_by_name) )        
    
    # when there are not args
    
    products = Products.query.filter_by(is_sell=False).all()
    
    for p in products:
        
        p.categories = p.categories_rel.name
    
    return jsonify( products_schema.dump(products) )


# Seed for add categories and products in databases
@bp.route("/seed-shop", methods=["GET"])
def seed_products():
    for c in categories_seed:
        categories = Categories()
        categories.name = c

        db.session.add(categories)
        db.session.commit()
    

    for p in products_seed:
        products = Products()
        
        products.name = p["name"]
        products.price = p["price"]
        products.description = ''
        products.imagehd = p["imagehd"]
        products.image = p["image"]
        products.is_sell = p["is_sell"]        
        products.categories = p["category"]
        
        db.session.add(products)
        db.session.commit()
        
        
    
    return jsonify({"message": "Seed Success"})
