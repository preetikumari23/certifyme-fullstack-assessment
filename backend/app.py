from flask import Flask
from flask_cors import CORS
from config import Config
from models import db
from routes.auth import auth_bp
from routes.opportunity import opp_bp

app = Flask(__name__)
from datetime import timedelta
app.permanent_session_lifetime = timedelta(days=7)
app.config.from_object(Config)

CORS(app, supports_credentials=True)

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(auth_bp)
app.register_blueprint(opp_bp)

if __name__ == "__main__":
    app.run(debug=True)