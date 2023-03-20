from flask import Blueprint, jsonify, request
from .seed_products import products as products_seed
from .models import Products
from src.config.db import db
from .schemas import ProductsSchemas


bp = Blueprint("products", __name__, url_prefix="/api")
product_schema = ProductsSchemas()
products_schema = ProductsSchemas(many=True)


@bp.route("/products", methods=["GET"])
def products_list():
    search = None
            
    try:
        search = request.args.get("search")
    except :
        search = None


    if search is not None:
        products_by_name = Products.query.filter(Products.name.ilike("%" + search + "%")).all()
        
        products_by_name_count = Products.query.filter(Products.name.ilike("%" + search + "%")).count()
        
        print(products_by_name_count)
        if products_by_name_count <= 0:
            return jsonify({
                "message": "No existen productos con estas caracteristicas"
            })
        
        
        return jsonify( products_schema.dump( products_by_name ) )
    
    products = Products.query.all()
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
        
        db.session.add(products)
        db.session.commit()
        
        
        print(p)
        


        
                
    
    return jsonify( {} )




