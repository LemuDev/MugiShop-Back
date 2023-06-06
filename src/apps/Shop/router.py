from flask import Blueprint, jsonify, request, redirect
from .seed_products import products as products_seed
from .seed_categories import categories as categories_seed

from .models import Products, Categories, CartItems, Cart
from src.apps.Auth.models import Users
from src.config.db import db
from .schemas import ProductsSchemas, CategoriesSchemas, CartItemSchemas, ProductSellSchemas
import secrets
import ast
 

from flask_jwt_extended import jwt_required, get_jwt_identity

import requests


bp = Blueprint("products", __name__, url_prefix="/api")
# Produsts Schemas for one or multiple products
product_schema = ProductsSchemas()
products_schema = ProductsSchemas(many=True)

# category Schemas for one or multiple Categories
category_schema = CategoriesSchemas()
categories_schema = CategoriesSchemas(many=True)


# End Point for see all products
@bp.route("/products", methods=["GET"])
def products_list():
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


# Endpoint for see all categories
@bp.route("/categories", methods=["GET"])
def categories_list():
    categories = Categories.query.all()

    return jsonify(categories_schema.dump(categories))



# End point for add cart
# jwt is required
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


# EndPoint for see the cart
# jwt is required
@bp.route("/cart", methods=["GET"])
@jwt_required()
def cart_list():
    current_user = get_jwt_identity()
    user_by_email = Users.query.filter_by(email = current_user).one_or_none()
    
    cart_by_user = Cart.query.filter_by(user_id = user_by_email.id).one_or_none()
    
    cart_items = CartItems.query.filter_by(cart_id=cart_by_user.id).filter_by(is_sell=False).all()
    
    cart = []
    for c_i in cart_items:
        
        product = Products.query.filter_by(id=c_i.product_id).first()
     
        cart.append({
            "id":c_i.id,
            "product": product.name,
            "price": product.price,
            "product_img": product.image
        })
        
       
    
    cart_serializer = CartItemSchemas(many=True)
    
    
    return jsonify(cart_serializer.dump(cart))

# EndPoint for delete the cart items
# jwt is required
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
        

# Generate order (link pay)
@bp.route("/create-order", methods=["POST"])
@jwt_required()
def GoPay():
    current_user = get_jwt_identity()
    token = get_paypal_token()
    token = token["access_token"]

    user_by_email = Users.query.filter_by(email=current_user).one_or_none()
    cart_by_user = Cart.query.filter_by(user_id=user_by_email.id).one_or_none()
    cart_items = CartItems.query.filter_by(cart_id=cart_by_user.id).filter_by(is_sell=False) 

    if cart_items.count() <= 0:
        print(cart_items)
        print(cart_items)
        
        return jsonify(error="No tienes productos agregados en el carrito")


    total = 0
    id_for_produts = []
    
    for item in cart_items:
        id_product = item.product_id
        
        id_for_produts.append(id_product)
        
        product = Products.query.get(id_product)
        
        
        total += product.price


    headers = {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',

        'PayPal-Request-Id': secrets.token_hex(32),
        'Authorization': 'Bearer ' + token,
    }
    
    reference = {
        "user": user_by_email.id,
        "products": id_for_produts
    }
    
    reference = str(reference)
   
    # "cancel_url": "https://example.com/cancelUrl" 
    data = '{ "intent": "CAPTURE", "purchase_units": [ {"reference_id" : "'+ reference + '", "amount": { "currency_code": "USD", "value": "' + str(total) + '" } } ], "payment_source": { "paypal": { "experience_context": { "payment_method_preference": "IMMEDIATE_PAYMENT_REQUIRED", "payment_method_selected": "PAYPAL", "brand_name": "EXAMPLE INC", "locale": "en-US", "landing_page": "LOGIN", "user_action": "PAY_NOW", "return_url": "http://127.0.0.1:8000/api/confirm-pay"} } } }'
    
    response = requests.post('https://api-m.sandbox.paypal.com/v2/checkout/orders', headers=headers, data=data)
    
    response=response.json()

    link_pay = response["links"][1]["href"]

    return jsonify(link_pay=link_pay)

@bp.route("/confirm-pay", methods=["GET"])
def confirmPay():
    token_args = request.args.get("token", None)
    PayerID = request.args.get("PayerID", None)

    if token_args == None or PayerID == None:
        return jsonify(error="Debes de pagar para acceder")
    
    
    response = getOrder(token_args)
    
    if not "status" in response:
        return jsonify(error="No se puede confirmar pago debes de pagar para confirmar---")
    else:
        if response["status"] == "COMPLETED":
 
            reference = response["purchase_units"][0]["reference_id"]
            reference = ast.literal_eval(reference)
            
            
            user_id = reference["user"]
            user_id = int(user_id)
            products_ids = reference["products"]
            
            print("User_id:", user_id)
            print("products ids:", products_ids)
            
            for id in products_ids:
                print("Product-id:", id)
                product = Products.query.get(id)
                product.is_sell = True
                db.session.commit()
                
                
                cart = Cart.query.filter_by(user_id=user_id).one_or_none()
                cart_items = CartItems.query.filter_by(product_id=id).filter_by(cart_id=cart.id).filter_by(is_sell=False).all()

                for item in cart_items:
                    
                    print(item)
                    
                    item.is_sell = True

                    
                    db.session.commit()
                
                
                

            return redirect("http://127.0.0.1:5173/profile")
        else:
            return jsonify(error="No se pudo confirmar el pago" )    



# get the order payed (Link for pay)
def getOrder(id_order):
    token = get_paypal_token()
    token = token["access_token"]
    
    
    headers = {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
        'PayPal-Request-Id': '7b92603e-77ed-4896-8e78-5dea2050476a',
        'Authorization':  'Bearer ' + token
    }
    
    response = requests.post(f'https://api-m.sandbox.paypal.com/v2/checkout/orders/{id_order}/capture', headers=headers)
    response = response.json()
    
    
    return response

# Get the paypal token  
def get_paypal_token():
    auth = ('AYJxnaEndV8YqpfEONJaUE3R07Qoetbn9O9Xpl_cX6Ii53sUuI4FH4pd-MruXY1pUO_Ai46oct9eDuO_', 'EIgOCaF8UM1LKuJy6XERI8ByZg3gTWAkhF_JaDfi_AiHclXTsRijTVGCvsy4Sse_mbzGXyRKBE1TcktF')
    
    

    data = {
        'grant_type': 'client_credentials',
    }

    response = requests.post(
        'https://api-m.sandbox.paypal.com/v1/oauth2/token', 
        data=data, 
        auth=auth
    )
    
    response = response.json()
        
    return response



# Get my nfts by user using JWT
@bp.route("/my-nfts", methods=["GET"])
@jwt_required()
def getMyNfts():
    current_user = get_jwt_identity()
    productSellSchemas = ProductSellSchemas(many=True)
    
    user_by_email = Users.query.filter_by(email=current_user).one_or_none()
    
    if user_by_email == None:
        return jsonify(msg="El usuario no es valido")

    cart_by_user = Cart.query.filter_by(user_id=user_by_email.id).one_or_none()
    items_cart = CartItems.query.filter_by(is_sell=True).filter_by(cart_id=cart_by_user.id)
    items_cart = items_cart.all()    
    
    nfts=[]
        
    for item in items_cart:
        product_by_id = Products.query.filter_by(id=item.product_id).one_or_none()
                
        nfts.append(product_by_id)
    
    
    for nft in nfts:
        nft.categories = nft.categories_rel.name
        
    
    nfts = productSellSchemas.dump(nfts)
    return jsonify(nfts=nfts)
