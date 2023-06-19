from flask import Blueprint, jsonify
from flask import request

import datetime
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from .model import Users
from src.apps.modules.cart.model import Cart

from .schemas import UserValidator, User_Schema, EditProfileValidator
from src.config.db import db

from werkzeug.security import generate_password_hash, check_password_hash


# Bluepint main app
bp = Blueprint('user', __name__, url_prefix="/api")


# Endpoint for register
# Here You can register new User
@bp.route("/register", methods=["POST"])
def register():
    if not request.is_json:
        
        return jsonify({
            "Error": "Los datos Deben de ser un Json. Datos No procesables"
        }, 400)
    
    data = request.json
    
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    password = data.get("password")
    
    if first_name == None or last_name == None or email == None or password == None:
        return jsonify({
            "Error": "No se pasan los datos necesarios para crear un usuario"
        }), 400
    
    new_user_data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password
    }

    errors = UserValidator().validate(data=new_user_data)


    if len(errors) >= 1:

        return jsonify(errors= errors), 400
    

    user_by_email_count = Users.query.filter_by(email=email).count()

    if user_by_email_count >= 1:
        return jsonify({
            "errors": {
                "email": ["Este email ya esta registrado"]
            }
        }), 400


    password_hash = generate_password_hash(password)

    new_user = Users(
        first_name=first_name,
        last_name=last_name,
        email=email ,
        password=password_hash,
        is_admin = False
    )
    
    db.session.add(new_user)
    db.session.commit()
  
    # Crear Carrito 
    user_id = Users.query.filter_by(email = email).first()
  
    create_cart = Cart(user_id = user_id.id )
    db.session.add(create_cart)
    db.session.commit()
         
         
    
    access_token = create_access_token(identity=email, expires_delta=datetime.timedelta(days=20))
    return jsonify(access_token=access_token)



# Endpoint for Login
# here you can Log In with your user
@bp.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        
        return jsonify({
            "Error": "Los datos Deben de ser un Json. Datos No procesables"
        }, 400)
    
    
    data = request.json

    email = data.get("email")
    password = data.get("password")
    
    if email == None or password == None:
        return jsonify(error="No se pasan los datos necesarios")
    
    
    user_by_email = Users.query.filter_by(email=email).first()

    if user_by_email == None:
        
        return jsonify(error= "Email o contraseña incorrectos"), 400
    

    if check_password_hash(password=password, pwhash=user_by_email.password):
        
        access_token = create_access_token(identity=email, expires_delta=datetime.timedelta(days=20))
        return jsonify(access_token=access_token)
    

   
    return jsonify(error="Email o contraseña incorrectos"), 400





#  Endpoint for profile
# here you can request the profile data
# For need a JWT
@bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    user_by_email = Users.query.filter_by(email=current_user).first()

    user_schema = User_Schema()
    
    return user_schema.dumps(user_by_email)


@bp.route("/profile", methods=["PUT"])
@jwt_required()
def edit_profile():
    current_user = get_jwt_identity()
    
    first_name = request.json.get("first_name", None)
    last_name = request.json.get("last_name", None)
    
    user_by_email = Users.query.filter_by(email = current_user).one_or_none()
    
    if first_name == None and last_name == None:
        return jsonify(error="No se pudo editar; debe mandar almenos un dato a editar")
        
    if user_by_email == None:
        return jsonify(error="El usuario que se quiere editar no existe")


    else:
        user = Users.query.get(user_by_email.id)
        
        edit_data={
            "first_name": first_name,
            "last_name": last_name
        }

        errors = EditProfileValidator().validate(data=edit_data)

        if len(errors) >= 1:

            return jsonify(errors= errors), 400
                
                
        user.first_name=first_name
        user.last_name=last_name
        db.session.commit()
            
        return jsonify(message="El perfil fue editado correctamente")
