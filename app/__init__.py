from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import logging

db = SQLAlchemy()
api = Api()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/library'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    
    logging.basicConfig(level=logging.DEBUG)
    app.logger.info('Starting the application')

    with app.app_context():
        from . import routes, api_routes
        routes.init_routes(app)

        api.init_app(app)
        api_routes.init_api(api)
        
        app.logger.info('Routes and API initialized')
        db.create_all()

    return app