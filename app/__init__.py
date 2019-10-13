# -*- coding:utf-8 -*-

from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app.api import bp as api_bp
from app.project import bp as project_bp
from app.runner import bp as runner_bp
app.register_blueprint(api_bp)
app.register_blueprint(project_bp)
app.register_blueprint(runner_bp)

