from flask import Flask
from app.routes.home import home_bp
from app.routes.intruder import intruder_bp
from app.routes.dilemma import dilemma_bp
from app.routes.party import party_bp

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(home_bp)
    app.register_blueprint(intruder_bp)
    app.register_blueprint(dilemma_bp)
    app.register_blueprint(party_bp)

    return app
