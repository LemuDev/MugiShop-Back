from src import app
from decouple import config

app.config["SECRET_KEY"] = config("SECRET_KEY")






if __name__ == '__main__':
    app.run(debug=config("DEBUG"), port=8000)    


