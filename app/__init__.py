from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/library'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    logging.basicConfig(level=logging.DEBUG)
    app.logger.info('Starting the application')

    with app.app_context():
        from . import routes
        routes.init_routes(app)
        
        app.logger.info('Routes initialized')
        db.create_all()

    return app