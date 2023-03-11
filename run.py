from src import app
import os


app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]



if __name__ == '__main__':
    app.run(debug=True, port=8000)    


