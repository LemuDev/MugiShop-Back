from flask import Blueprint, jsonify, request
from .seed_products import products as products_seed
from .seed_categories import categories as categories_seed

from .models import Products, Categories
from src.config.db import db
from .schemas import ProductsSchemas, CategoriesSchemas


from flask_jwt_extended import jwt_required


bp = Blueprint("products", __name__, url_prefix="/api")

product_schema = ProductsSchemas()
products_schema = ProductsSchemas(many=True)

category_schema = CategoriesSchemas()
categories_schema = CategoriesSchemas(many=True)


@bp.route("/products", methods=["GET"])
def products_list():
    name = request.args.get("name")
    category = request.args.get("category")



    if name is not None:
        products_by_name = Products.query.filter(Products.name.ilike("%" + name + "%")).all()
        products_by_name_count = Products.query.filter(Products.name.ilike("%" + name + "%")).count()
        
        if category is not None:
            products_by_name = Products.query.filter(Products.name.ilike("%" + name + "%")).filter_by(categories=category).all()
            products_by_name_count = Products.query.filter(Products.name.ilike("%" + name + "%")).filter_by(categories=category).count()
        
        if products_by_name_count  >= 1:
      
            for p in products_by_name:
                p.categories = p.categories_rel.name
                
        return jsonify( products_schema.dump(products_by_name) )
    else:
        if category is not None:
            products_by_name = Products.query.filter_by(categories=category).all()
            products_by_name_count = Products.query.filter_by(categories=category).count()
        
        
            if products_by_name_count  >= 1:

                for p in products_by_name:
                    p.categories = p.categories_rel.name        
            
            return jsonify( products_schema.dump(products_by_name) )        
    



    # when there are not args
    
    products = Products.query.filter().all()
    
    for p in products:
        
        p.categories = p.categories_rel.name
    
    return jsonify( products_schema.dump(products) )

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
        products.image = p["image"]
        products.is_sell = p["is_sell"]        
        products.categories = p["category"]
        
        db.session.add(products)
        db.session.commit()
        
        
    
    return jsonify({"message": "Seed Success"})

@bp.route("/categories", methods=["GET"])
def categories_list():
    categories = Categories.query.all()


    
    return jsonify(categories_schema.dump(categories))



@bp.route("/cart", methods=["GET"])
def CartData():
    return {}


@bp.route("/cart", methods=["POST"])
def CreateCart():
    return {}


@bp.route("/cart", methods=["DELETE"])
def CartDeleteCartItem():
    return {}


