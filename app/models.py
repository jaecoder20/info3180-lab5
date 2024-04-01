import datetime
from . import db

class Movies(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    poster_url = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, title, description, poster_url):
        self.title = title
        self.description = description
        self.poster_url = poster_url


    def __repr__(self):
        return f"Movie({self.title})"