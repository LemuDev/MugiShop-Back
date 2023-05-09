from flask import Blueprint, jsonify
from flask import request

import datetime
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Users
from src.apps.Shop.models import Cart

from .schemas import UserValidator, User_Schema
from src.config.db import db

from werkzeug.security import generate_password_hash, check_password_hash


# Bluepint main app
bp = Blueprint('auth', __name__, url_prefix="/api")


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

    create_user = Users()
    create_user.first_name = first_name
    create_user.last_name = last_name
    create_user.email = email
    create_user.password = password_hash
    create_user.is_admin = False
    
    db.session.add(create_user)
    db.session.commit()
  
    # Crear Carrito 
    user_id = Users.query.filter_by(email = email).first()
  
    create_cart = Cart()
    create_cart.user_id = user_id.id  
    db.session.add(create_cart)
    db.session.commit()
         
         
    
    access_token = create_access_token(identity=email, expires_delta=datetime.timedelta(days=20))
    return jsonify(access_token=access_token)



# Endpoint for Login
# here you can Log In with your user
@bp.route("/login", methods=["POST"])
def login():
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
        
    if not request.is_json:
        return jsonify(error="El formato no es adecuado")
    else:   
        errors = {
            "first_name":[],
            "last_name":[]
        }
        
        first_name = request.json.get("first_name", None)
        last_name = request.json.get("last_name", None)
        
        
        if first_name == None:
            errors["first_name"].append("EL nombre es requerido")
        else:
            first_name = str(first_name)
            if len(first_name.strip()) < 0 or first_name == None:
                errors["first_name"].append("EL nombre es requerido")

            elif len(first_name.strip()) > 60:
                errors["first_name"].append("El nombre debe de ser menor a 60 caracteres")
        
        if last_name == None:
            errors["last_name"].append("EL Apellido es requerido")
            
        else:
            last_name = str(last_name)
            
            
            if len(last_name.strip()) < 0 or last_name == None:
                errors["last_name"].append("EL Apellido es requerido")

            elif len(last_name.strip()) > 60:
                errors["last_name"].append("El Apellido debe de ser menor a 60 caracteres")
        
        
        print(errors)
        
        if len( errors["first_name"] ) >= 1 or len(errors["last_name"]) >= 1:
            if len(errors["first_name"]) >= 1 and len(errors["last_name"]) <= 0:
                del errors["last_name"]
                return jsonify(errors=errors)
        

            elif len(errors["last_name"]) >= 1 and len(errors["first_name"]) <= 0:
                del errors["first_name"]
                return jsonify(errors=errors)

            else:
                return jsonify(errors=errors)
        
        else:    
            user_by_email = Users.query.filter_by(email=current_user).one_or_none()


    
    user_by_email = Users.query.filter_by(email=current_user).first()

@bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    current_user = get_jwt_identity()


    
    user_by_email = Users.query.filter_by(email=current_user).first()


            user = Users.query.get(user_by_email.id)
            user.first_name = first_name
            user.last_name = last_name


            db.session.commit()
            
            return jsonify(message="El perfil fue editado correctamente")

    user_schema = User_Schema()
    print(user_by_email)
    
    
    return user_schema.dumps(user_by_email)

