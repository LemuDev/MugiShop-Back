from flask import Blueprint, jsonify, request
from .seed_products import products as products_seed
from .seed_categories import categories as categories_seed

from .models import Products, Categories
from src.config.db import db
from .schemas import ProductsSchemas, CategoriesSchemas


bp = Blueprint("products", __name__, url_prefix="/api")

product_schema = ProductsSchemas()
products_schema = ProductsSchemas(many=True)

category_schema = CategoriesSchemas()
categories_schema = CategoriesSchemas(many=True)


@bp.route("/products", methods=["GET"])
def products_list():
    query = None
            
    try:
        query = request.args.get("query")
    except :
        query = None


    if query is not None:
        products_by_name = Products.query.filter(Products.name.ilike("%" + query + "%")).all()
        products_by_name_count = Products.query.filter(Products.name.ilike("%" + query + "%")).count()
        
        if products_by_name_count <= 0:
            return jsonify({
                "message": "No existen productos con estas caracteristicas"
            })
        
        for p in products_by_name:
            p.categories = p.categories_rel.name
            
        return jsonify( products_schema.dump( products_by_name ) )
    
    products = Products.query.all()
    for p in products:

        p.categories = p.categories_rel.name
        
    return jsonify( products_schema.dump(products) )



@bp.route("/seed-products", methods=["GET"])
def seed_products():
    
        
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
        
        
    
    return jsonify({"seed": products_seed})


@bp.route("/seed-categories", methods=["GET"])
def seed_categories():
    
    for c in categories_seed:
        categories = Categories()
        categories.name = c

        db.session.add(categories)
        db.session.commit()
    
        
    
    return jsonify({})

@bp.route("/categories", methods=["GET"])
def categories_list():
    categories = Categories.query.all()


    
    return jsonify(categories_schema.dump(categories))


