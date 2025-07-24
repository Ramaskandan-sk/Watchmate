from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import uuid

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with watchlist items
    watchlist_items = db.relationship('WatchlistItem', backref='user', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'

class WatchlistItem(db.Model):
    __tablename__ = 'watchlist'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(10), nullable=False)  # 'Movie', 'Anime', or 'Series'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<WatchlistItem {self.title}>'