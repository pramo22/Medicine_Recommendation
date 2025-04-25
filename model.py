from flask_login import UserMixin 
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    security_answer = db.Column(db.String(100), nullable=False)
    # Changed the backref to 'user_reviews' for uniqueness
    reviews = db.relationship('Reviews', backref='user_reviews', lazy=True)  # Changed backref name

    def __init__(self, user_id, username, email, password, security_answer):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.security_answer = security_answer

    def get_id(self):
        return self.user_id


class Reviews(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    review_text = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.String(80), db.ForeignKey('users.user_id'), nullable=False)

    def __init__(self, review_text, user_id):
        self.review_text = review_text
        self.user_id = user_id