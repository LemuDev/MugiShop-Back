from flask import Blueprint, jsonify, request
from .seed_products import products as products_seed
from .seed_categories import categories as categories_seed

from .models import Products, Categories, CartItems, Cart
from src.apps.Auth.models import Users
from src.config.db import db
from .schemas import ProductsSchemas, CategoriesSchemas, CartItemSchemas


from flask_jwt_extended import jwt_required, get_jwt_identity


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




@bp.route("/cart", methods=["POST"])
@jwt_required()
def add_to_cart():
    current_user = get_jwt_identity()
    
    if not request.is_json:
        
        return jsonify({
            "error": "El formato de envio de datos no es correcto"
        }), 400
            
    else:
        data = request.json

        user_by_email = Users.query.filter_by(email = current_user).first()

        product_id = data.get("product")        
        
        try:
            product_id = int(product_id)       
        except:
            
            return jsonify(error="El tipo de dato del prodcto debe de ser numerico"), 400 
        

        product_by_id = Products.query.filter_by(id=product_id).one_or_none()
        
        if product_by_id == None:
            
            return jsonify(error="El producto que se intenta agregar no existe"), 404

        if product_by_id.is_sell == True:
           
            return jsonify(error="El producto que se intenta agregar ya fue vendido, las imagenes solo se venden una vez"), 400


        cart_by_user = Cart.query.filter_by(user_id=user_by_email.id).one_or_none()
        is_item_in_cart = CartItems.query.filter_by(cart_id=cart_by_user.id).filter_by(product_id=product_by_id.id).count()
        
        if is_item_in_cart >= 1:
            
            return jsonify(error="El producto que se intenta agregar ya esta en el carrito"), 400
        
        item_in_cart = CartItems()
        item_in_cart.product_id = product_id
        item_in_cart.cart_id = cart_by_user.id  
        
        db.session.add(item_in_cart)
        db.session.commit()          
    
        return jsonify(message=f"{product_by_id.name} fue Agregado al carrito") 

@bp.route("/cart", methods=["GET"])
@jwt_required()
def cart_list():
    current_user = get_jwt_identity()
    user_by_email = Users.query.filter_by(email = current_user).one_or_none()
    
    cart_by_user = Cart.query.filter_by(user_id = user_by_email.id).one_or_none()
    
    cart_items = CartItems.query.filter_by(cart_id=cart_by_user.id).all()
    
    cart = []
    for c_i in cart_items:
        
        product = Products.query.filter_by(id=c_i.product_id).first()
     
        cart.append({
            "id":c_i.id,
            "product": product.name,
            "product_img": product.image
        })
        
        
        print("product_img", c_i.cart.user_id)
    
    
    
    cart_serializer = CartItemSchemas(many=True)
    
    
    return jsonify(cart_serializer.dump(cart))





@bp.route("/cart", methods=["DELETE"])
@jwt_required()
def delete_item_cart():
    current_user = get_jwt_identity()
    
    if not request.is_json:
        
        return jsonify({
            "error": "El formato de envio de datos no es correcto"
        }), 400
        
    else:    
        data = request.json
        product_item_id = data.get("id")
        
        user = Users.query.filter_by(email=current_user).first()
        
        try:
            product_item_id = int(product_item_id)
        except :    
            return jsonify(error="El tipo de dato del prodcto debe de ser numerico"), 400 
        
        
        
        cart = Cart.query.filter_by(user_id=user.id).first()

        product_item = CartItems.query.filter_by(id=product_item_id).filter_by(cart_id=cart.id).one_or_none()

        if product_item == None:
            return jsonify(error="El producto que se intenta eliminar no esta agregado"), 404



        db.session.delete(product_item)
        db.session.commit()
        
        product_name = Products.query.filter_by(id=product_item.product_id).first()
        product_name = product_name.name


        return jsonify(message=f"Producto {product_name} eliminado correctamente")
        

        
            