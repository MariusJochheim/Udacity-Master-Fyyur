#----------------------------------------------------------------------------#
# Venue routes
#----------------------------------------------------------------------------#

from datetime import datetime

from flask import render_template, request, flash, redirect, url_for

from extensions import app, db
from forms import VenueForm
from models import Venue, Show, Artist


@app.route('/venues')
def venues():
    now = datetime.utcnow()
    upcoming_counts = (
        db.session.query(
            Show.venue_id,
            db.func.count(Show.id).label('num_upcoming_shows'),
        )
        .filter(Show.start_time > now)
        .group_by(Show.venue_id)
        .subquery()
    )
    venues_with_counts = (
        db.session.query(
            Venue.id,
            Venue.name,
            Venue.city,
            Venue.state,
            db.func.coalesce(upcoming_counts.c.num_upcoming_shows, 0).label('num_upcoming_shows'),
        )
        .outerjoin(upcoming_counts, Venue.id == upcoming_counts.c.venue_id)
        .all()
    )
    areas = {}
    for venue in venues_with_counts:
        key = (venue.city, venue.state)
        area = areas.get(key)
        if area is None:
            area = {"city": venue.city, "state": venue.state, "venues": []}
            areas[key] = area
        area["venues"].append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": venue.num_upcoming_shows,
        })
    data = list(areas.values())
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term = request.form.get('search_term', '').strip()
    now = datetime.utcnow()
    upcoming_counts = (
        db.session.query(
            Show.venue_id,
            db.func.count(Show.id).label('num_upcoming_shows'),
        )
        .filter(Show.start_time > now)
        .group_by(Show.venue_id)
        .subquery()
    )
    venues = (
        db.session.query(
            Venue.id,
            Venue.name,
            db.func.coalesce(upcoming_counts.c.num_upcoming_shows, 0).label('num_upcoming_shows'),
        )
        .outerjoin(upcoming_counts, Venue.id == upcoming_counts.c.venue_id)
        .filter(db.func.lower(Venue.name).like(f"%{search_term.lower()}%"))
        .all()
    )
    response = {
        "count": len(venues),
        "data": [
            {
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": venue.num_upcoming_shows,
            }
            for venue in venues
        ],
    }
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    venue = Venue.query.get(venue_id)
    now = datetime.utcnow()
    genres = venue.genres or []
    if isinstance(genres, (list, tuple)):
        if genres and all(isinstance(g, str) and len(g) == 1 for g in genres):
            genres = "".join(genres)
        elif len(genres) == 1 and isinstance(genres[0], str):
            genres = genres[0]
    if isinstance(genres, str):
        genres = [g.strip() for g in genres.strip("{}").split(",") if g.strip()]
    shows = (
        db.session.query(Show, Artist)
        .join(Artist, Show.artist_id == Artist.id)
        .filter(Show.venue_id == venue_id)
        .all()
    )
    past_shows = []
    upcoming_shows = []
    for show, artist in shows:
        show_data = {
            "artist_id": artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": show.start_time.isoformat(),
        }
        if show.start_time > now:
            upcoming_shows.append(show_data)
        else:
            past_shows.append(show_data)
    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website_link,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }
    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    venue = Venue(
        name=request.form['name'],
        city=request.form['city'],
        state=request.form['state'],
        address=request.form['address'],
        phone=request.form.get('phone'),
        image_link=request.form.get('image_link'),
        facebook_link=request.form.get('facebook_link'),
        genres=request.form.getlist('genres'),
        website_link=request.form.get('website_link'),
        seeking_talent=bool(request.form.get('seeking_talent')),
        seeking_description=request.form.get('seeking_description'),
    )
    data = venue
    try:
        db.session.add(venue)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except Exception:
        db.session.rollback()
        flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)
    if venue:
        form.name.data = venue.name
        form.city.data = venue.city
        form.state.data = venue.state
        form.address.data = venue.address
        form.phone.data = venue.phone
        form.image_link.data = venue.image_link
        form.genres.data = venue.genres
        form.facebook_link.data = venue.facebook_link
        form.website_link.data = venue.website_link
        form.seeking_talent.data = venue.seeking_talent
        form.seeking_description.data = venue.seeking_description
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    venue = Venue.query.get(venue_id)
    if venue:
        venue.name = request.form['name']
        venue.city = request.form['city']
        venue.state = request.form['state']
        venue.address = request.form['address']
        venue.phone = request.form.get('phone')
        venue.image_link = request.form.get('image_link')
        venue.facebook_link = request.form.get('facebook_link')
        venue.genres = request.form.getlist('genres')
        venue.website_link = request.form.get('website_link')
        venue.seeking_talent = bool(request.form.get('seeking_talent'))
        venue.seeking_description = request.form.get('seeking_description')
    try:
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully updated!')
    except Exception:
        db.session.rollback()
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')
    return redirect(url_for('show_venue', venue_id=venue_id))


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        venue = Venue.query.get(venue_id)
        if venue:
            db.session.delete(venue)
            db.session.commit()
            flash('Venue was successfully deleted!')
        else:
            flash('Venue not found.')
    except Exception:
        db.session.rollback()
        flash('An error occurred. Venue could not be deleted.')
    return redirect(url_for('index'))
