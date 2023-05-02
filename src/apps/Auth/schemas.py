from marshmallow import Schema, fields
from marshmallow.validate import Length

class UserValidator(Schema):    
    first_name = fields.Str(required=True, 
        validate=[
            Length(max=100, error="El Nombre debe de tener menos de 100 caracteres"),
            Length(min=1, error="El Nombre no puede estar vacio")
        ],
        
        error_messages={
          'required': 'El Nombre es requerido'
        }
    )
    
    last_name = fields.Str(required=True, 
        validate=[
            Length(max=100, error="El Apellidos debe de tener menos de 100 caracteres"),
            Length(min=1, error="El apellido no puede estar vacio")
        ],
        
        error_messages={
          'required': 'El Apellido es requerido'
        }
    )
    
    email = fields.Email(
        required=True,
        
        validate=[
            Length(max=255, error="El Email debe de tener menos de 255 caracteres"),
            Length(min=1, error="El email no puede estar vacio")
        ],
        
        error_messages={
          'required': 'El email es requerido.', 
          'invalid': 'El email no es valido'
        }
    )
    
    password = fields.Str(
        required=True, 
        validate=[
            Length(max=100, error="La contraseña debe de tener menos de 100 caracteres"),
            Length(min=8, error="La contraseña debe de tener mas de 8 caracteres")
        ],
        
        error_messages={
          'required': 'La contraseña es requerida'
        }
    )
    



class User_Schema(Schema):
    class Meta:
        fields=("id", "first_name", "last_name", "email")