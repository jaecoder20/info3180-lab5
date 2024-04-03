from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_migrate import Migrate
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
#app.config['WTF_CSRF_ENABLED'] = False
migrate = Migrate(app, db) 
from app import models

from app import views
