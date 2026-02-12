from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Song(db.Model):
    """Song model representing the songs table"""
    
    __tablename__ = 'songs'
    
    # Primary key
    index = db.Column(db.Integer, primary_key=True)
    
    # Basic information
    id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    
    # Audio features
    danceability = db.Column(db.Float)
    energy = db.Column(db.Float)
    loudness = db.Column(db.Float)
    acousticness = db.Column(db.Float)
    instrumentalness = db.Column(db.Float)
    liveness = db.Column(db.Float)
    valence = db.Column(db.Float)
    
    # Musical attributes
    tempo = db.Column(db.Float)
    key = db.Column(db.Integer)
    mode = db.Column(db.Integer)
    time_signature = db.Column(db.Integer)
    
    # Structural information
    duration_ms = db.Column(db.Integer)
    num_bars = db.Column(db.Integer)
    num_sections = db.Column(db.Integer)
    num_segments = db.Column(db.Integer)
    
    # Classification
    class_field = db.Column('class', db.Integer)  # 'class' is a Python keyword, so we use 'class_field'
    
    # User rating
    star_rating = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Song {self.title}>'
    
    def to_dict(self):
        """Convert song object to dictionary"""
        return {
            'index': self.index,
            'id': self.id,
            'title': self.title,
            'danceability': self.danceability,
            'energy': self.energy,
            'loudness': self.loudness,
            'acousticness': self.acousticness,
            'instrumentalness': self.instrumentalness,
            'liveness': self.liveness,
            'valence': self.valence,
            'tempo': self.tempo,
            'key': self.key,
            'mode': self.mode,
            'time_signature': self.time_signature,
            'duration_ms': self.duration_ms,
            'num_bars': self.num_bars,
            'num_sections': self.num_sections,
            'num_segments': self.num_segments,
            'class': self.class_field,
            'star_rating': self.star_rating,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def validate_rating(rating):
        """Validate star rating value"""
        if not isinstance(rating, int):
            raise ValueError("Rating must be an integer")
        if rating < 0 or rating > 5:
            raise ValueError("Rating must be between 0 and 5")
        return True