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
    first_name = request.json.get("first_name")
    last_name = request.json.get("last_name")
    email = request.json.get("email")
    password = request.json.get("password")
    
    
    if first_name == None or last_name == None or email == None or password == None:
    
        return jsonify({
            "Error": "No se pasan los datos necesarios para crear un usuario"
        })
        
    else:
        first_name = first_name.strip()
        last_name = last_name.strip()
        email = email.strip()
        password = password.strip()
        

        
        new_user_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password
        }

        errors = UserValidator().validate(data=new_user_data)

   
        if len(errors) >= 1:
    
            return jsonify(errors= errors)
        
        else:
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
                
                
            if check_password_hash(password=password, pwhash=password_hash):
                
                access_token = create_access_token(identity=email, expires_delta=datetime.timedelta(days=20))
                return jsonify(access_token=access_token)
        
            return jsonify({
                "message": "Usuario Creado Correctamente"
            })
    
@bp.route("/login", methods=["POST"])
def login():
    email = request.json.get("email")
    password = request.json.get("password")
    
    user_by_email = Users.query.filter_by(email=email).first()

    if user_by_email == None:
        
        return jsonify(error= "Email o contraseña incorrectos")
    
    else:
        if check_password_hash(password=password, pwhash=user_by_email.password):
            
            access_token = create_access_token(identity=email, expires_delta=datetime.timedelta(days=20))
            return jsonify(access_token=access_token)
        
        else:
   
            return jsonify(error="Email o contraseña incorrectos")