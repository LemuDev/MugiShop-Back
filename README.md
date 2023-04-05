# MugiShop-Back

## Crear y activar Entorno virtual
+ virtualenv env
+ cd env/scripts
+ activate

## Instalar dependencias 
+ pip install -r requirements.txt

## Crear Tablas de los modelos
+ python
+ from src import app
+ from src.apps.Shop.models import *
+ from src.apps.Auth.models import *
+ from src.config.db import db
+ with app.app_context(): db.drop_all()
+ with app.app_context(): db.create_all()


## OJO Variables de entorno se pasan por privado
