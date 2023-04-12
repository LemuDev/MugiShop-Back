from flask import Blueprint, jsonify
from flask import request

import datetime
from flask_jwt_extended import create_access_token


from .models import Users
from .schemas import UserValidator
from src.config.db import db






from werkzeug.security import generate_password_hash, check_password_hash


bp = Blueprint('auth', __name__, url_prefix="/api")


@bp.route("/register", methods=["POST"])
def register():

    if not request.is_json:
        
        return jsonify({
            "Error": "No se pasan los datos necesarios para crear un usuario"
        })
    
    
    data = request.json
    
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    password = data.get("password")
    
    if first_name == None or last_name == None or email == None or password == None:
        return jsonify({
            "Error": "No se pasan los datos necesarios para crear un usuario"
        })
    
    
    new_user_data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password
    }

    errors = UserValidator().validate(data=new_user_data)


    if len(errors) >= 1:

        return jsonify(errors= errors)
    

    user_by_email_count = Users.query.filter_by(email=email).count()

    if user_by_email_count >= 1:
        return jsonify({
            "errors": {
                "email": ["Este email ya esta registrado"]
            }
        })


    password_hash = generate_password_hash(password)

    create_user = Users()
    create_user.first_name = first_name
    create_user.last_name = last_name
    create_user.email = email
    create_user.password = password_hash
    create_user.is_admin = False
    
    db.session.add(create_user)
    db.session.commit()
    
                
    access_token = create_access_token(identity=email, expires_delta=datetime.timedelta(days=20))
    return jsonify(access_token=access_token)


@bp.route("/login", methods=["POST"])
def login():
    data = request.json


    email = data.get("email")
    password = data.get("password")
    
    if email == None or password == None:
        return jsonify(error="No se pasan los datos necesarios")
    
    
    user_by_email = Users.query.filter_by(email=email).first()

    if user_by_email == None:
        
        return jsonify(error= "Email o contraseña incorrectos")
    

    if check_password_hash(password=password, pwhash=user_by_email.password):
        
        access_token = create_access_token(identity=email, expires_delta=datetime.timedelta(days=20))
        return jsonify(access_token=access_token)
    

   
    return jsonify(error="Email o contraseña incorrectos")