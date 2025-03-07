from flask import Flask
from .config import DevConfig,ProdConfig
from .routes import user_bp,expenses_bp,transfers_bp,alerts_bp,transaction_bp
from flask_sqlalchemy import SQLAlchemy
from .models import db
from flask_jwt_extended import JWTManager
from flask_mail import Mail,Message

mail = Mail()

def create_app():
    app = Flask(__name__)
  

    app.config.from_object(ProdConfig)
    app.register_blueprint(user_bp)
    app.register_blueprint(expenses_bp)
    app.register_blueprint(transfers_bp)
    app.register_blueprint(alerts_bp)
    app.register_blueprint(transaction_bp)
    #Initialize db
    with app.app_context():
        db.init_app(app)
        db.create_all()
    #Initialize JWT 
    jwt = JWTManager(app)
    mail.init_app(app)  
    mail.debug = True  # Forcefully set the debug attribute

    app.extensions['mail'] = mail  # Attach mail to app.extensions
 


    return app
