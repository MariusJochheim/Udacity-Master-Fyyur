#----------------------------------------------------------------------------#
# Artist routes
#----------------------------------------------------------------------------#

from datetime import datetime

from flask import render_template, request, flash, redirect, url_for

from extensions import app, db
from forms import ArtistForm
from models import Artist, Show, Venue


@app.route('/artists')
def artists():
    artists = (
        db.session.query(Artist.id, Artist.name)
        .order_by(Artist.id)
        .all()
    )
    data = [
        {"id": artist.id, "name": artist.name}
        for artist in artists
    ]
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    search_term = request.form.get('search_term', '').strip()
    now = datetime.utcnow()
    upcoming_counts = (
        db.session.query(
            Show.artist_id,
            db.func.count(Show.id).label('num_upcoming_shows'),
        )
        .filter(Show.start_time > now)
        .group_by(Show.artist_id)
        .subquery()
    )
    artists = (
        db.session.query(
            Artist.id,
            Artist.name,
            db.func.coalesce(upcoming_counts.c.num_upcoming_shows, 0).label('num_upcoming_shows'),
        )
        .outerjoin(upcoming_counts, Artist.id == upcoming_counts.c.artist_id)
        .filter(db.func.lower(Artist.name).like(f"%{search_term.lower()}%"))
        .all()
    )
    response = {
        "count": len(artists),
        "data": [
            {
                "id": artist.id,
                "name": artist.name,
                "num_upcoming_shows": artist.num_upcoming_shows,
            }
            for artist in artists
        ],
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    artist = Artist.query.get(artist_id)
    now = datetime.utcnow()
    genres = artist.genres or []
    if isinstance(genres, (list, tuple)):
        if genres and all(isinstance(g, str) and len(g) == 1 for g in genres):
            genres = "".join(genres)
        elif len(genres) == 1 and isinstance(genres[0], str):
            genres = genres[0]
    if isinstance(genres, str):
        genres = [g.strip() for g in genres.strip("{}").split(",") if g.strip()]
    shows = (
        db.session.query(Show, Venue)
        .join(Venue, Show.venue_id == Venue.id)
        .filter(Show.artist_id == artist_id)
        .all()
    )
    past_shows = []
    upcoming_shows = []
    for show, venue in shows:
        show_data = {
            "venue_id": venue.id,
            "venue_name": venue.name,
            "venue_image_link": venue.image_link,
            "start_time": show.start_time.isoformat(),
        }
        if show.start_time > now:
            upcoming_shows.append(show_data)
        else:
            past_shows.append(show_data)
    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website_link,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }
    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    if artist:
        form.name.data = artist.name
        form.city.data = artist.city
        form.state.data = artist.state
        form.phone.data = artist.phone
        form.image_link.data = artist.image_link
        form.genres.data = artist.genres
        form.facebook_link.data = artist.facebook_link
        form.website_link.data = artist.website_link
        form.seeking_venue.data = artist.seeking_venue
        form.seeking_description.data = artist.seeking_description
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    artist = Artist.query.get(artist_id)
    if artist:
        artist.name = request.form['name']
        artist.city = request.form['city']
        artist.state = request.form['state']
        artist.phone = request.form.get('phone')
        artist.image_link = request.form.get('image_link')
        artist.facebook_link = request.form.get('facebook_link')
        artist.genres = request.form.getlist('genres')
        artist.website_link = request.form.get('website_link')
        artist.seeking_venue = bool(request.form.get('seeking_venue'))
        artist.seeking_description = request.form.get('seeking_description')
    try:
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully updated!')
    except Exception:
        db.session.rollback()
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.')

    return redirect(url_for('show_artist', artist_id=artist_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    artist = Artist(
        name=request.form['name'],
        city=request.form['city'],
        state=request.form['state'],
        phone=request.form.get('phone'),
        image_link=request.form.get('image_link'),
        facebook_link=request.form.get('facebook_link'),
        genres=request.form.getlist('genres'),
        website_link=request.form.get('website_link'),
        seeking_venue=bool(request.form.get('seeking_venue')),
        seeking_description=request.form.get('seeking_description'),
    )
    data = artist
    try:
        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except Exception:
        db.session.rollback()
        flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')
