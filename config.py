from os import environ
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get(
    "DATABASE_URL", "postgresql://localhost:5432/dance"
)
if app.config["SQLALCHEMY_DATABASE_URI"].startswith("postgres://"):
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config[
        "SQLALCHEMY_DATABASE_URI"
    ].replace("postgres://", "postgresql://")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

if environ.get("TEST_RUNNING", 0):
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost:5432/dance_test"


db = SQLAlchemy(app)
migrate = Migrate(app, db)
