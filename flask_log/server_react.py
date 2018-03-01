from flask import Flask, current_app
from flask_login import LoginManager, login_manager
import websiteconfig as config
from handler_react import run_app
from flask_cors import CORS


login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "\protected"

def create_app():
    app = Flask(__name__)
    CORS(app,supports_credentials=True)
    app.debug = config.DEBUG
    app.config['SECRET_KEY'] = config.SECRET_KEY
    login_manager.init_app(app)
    run_app(app,login_manager)

    # will return none if doesnt match



    return app



if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0')
