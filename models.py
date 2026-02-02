#----------------------------------------------------------------------------#
# Models
#----------------------------------------------------------------------------#

from sqlalchemy.dialects.postgresql import ARRAY

from extensions import db


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), unique=True)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120), unique=True)
    genres = db.Column(ARRAY(db.String()), nullable=False)
    website_link = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean, default=False, nullable=False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship(
        'Show',
        back_populates='venue',
        cascade='all, delete-orphan',
        lazy=True,
    )


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), unique=True)
    genres = db.Column(ARRAY(db.String()), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120), unique=True)
    website_link = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean, default=False, nullable=False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship(
        'Show',
        back_populates='artist',
        cascade='all, delete-orphan',
        lazy=True,
    )


class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    venue = db.relationship('Venue', back_populates='shows')
    artist = db.relationship('Artist', back_populates='shows')
