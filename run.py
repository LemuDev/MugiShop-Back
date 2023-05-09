from src import app
from decouple import config


# Run Aplication 
if __name__ == '__main__':
    app.run(debug=config("DEBUG"), port=8000)    
