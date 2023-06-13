from flask import Blueprint
from flask import jsonify, request, redirect

from src.config.db import db
from .utils import get_paypal_token, getOrder

from decouple import config

# Jwt 
from flask_jwt_extended import get_jwt_identity, jwt_required

# Modules
from src.apps.modules.users.model import Users
from src.apps.modules.products.model import Products
from src.apps.modules.cart.model import Cart
from src.apps.modules.cart.model import CartItems


# Schemas used
from .schemas import ProductSellSchemas

import requests
import secrets
import ast


# Blueprint definition
bp=Blueprint("product-sell", __name__, url_prefix="/api")



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
   

    data = '{ "intent": "CAPTURE", "purchase_units": [ {"reference_id" : "'+ reference + '", "amount": { "currency_code": "USD", "value": "' + str(total) + '" } } ], "payment_source": { "paypal": { "experience_context": { "payment_method_preference": "IMMEDIATE_PAYMENT_REQUIRED", "payment_method_selected": "PAYPAL", "brand_name": "EXAMPLE INC", "locale": "en-US", "landing_page": "LOGIN", "user_action": "PAY_NOW", "return_url":'+ config("URL_CONFIRM_PAY") + '} } } }'
    
    response = requests.post(config("URL_GET_ORDER"), headers=headers, data=data)
    
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
            
        
            for id in products_ids:
                print("Product-id:", id)
                product = Products.query.get(id)
                product.is_sell = True
                db.session.commit()
                
                
                cart = Cart.query.filter_by(user_id=user_id).one_or_none()
                cart_items = CartItems.query.filter_by(product_id=id).filter_by(cart_id=cart.id).filter_by(is_sell=False).all()

                for item in cart_items:
                    item.is_sell = True
                                
                    db.session.commit()
                
            return redirect(config["URL_FRONTEND_PROFILE"])
        else:
            return jsonify(error="No se pudo confirmar el pago" )    


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
