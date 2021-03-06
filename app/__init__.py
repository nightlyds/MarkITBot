from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_mail import Mail

app = Flask(__name__)

app.config.from_object(Config)

mail = Mail(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

def _update_db(obj):
    db.session.add(obj)
    db.session.commit()
    return obj


from app import routes, models
