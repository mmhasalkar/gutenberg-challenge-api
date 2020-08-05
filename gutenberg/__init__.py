from flask import Flask
import logging
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from gutenberg.config import Config


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)


def create_app():
    cors = CORS(app)
    # db.init_app(app)

    FORMAT = '%(asctime)-15s [%(levelname)s] [%(filename)s:%(lineno)s]: %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO, filename="logs/service.out")

    from gutenberg.main.routes import main

    app.register_blueprint(main)

    return app