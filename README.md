# MugiShop-Back

## Si no tienes un virtualenv instalado
```
pip install -m virtualenv
```


## Crear y activar Entorno virtual
```
virtualenv env
```

```
cd env/scripts
```

```
activate
```

```
cd ../..
```

```
## Instalar dependencias 
```

```
pip install -r requirements.txt
```


## Crear Tablas de los modelos
```
python
```

```
from src import db_init
```

```
db_init()
```


## Correr server
```
python run.py
```


## OJO Variables de entorno se pasan por privado
