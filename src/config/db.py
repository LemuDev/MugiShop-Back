from flask_sqlalchemy import SQLAlchemy


# Config For SqlAlchemy

db = SQLAlchemy(session_options={"autoflush": False})