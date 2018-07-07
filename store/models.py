from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    artist = db.Column(db.String(255), nullable=False)
    cover_image_url = db.Column(db.String(255), nullable=False)
    bandcamp_url = db.Column(db.String(255), nullable=False)