#----------------------------------------------------------------------------#
# Show routes
#----------------------------------------------------------------------------#

from datetime import datetime

from flask import render_template, request, flash

from extensions import app, db
from forms import ShowForm
from models import Show, Venue, Artist


@app.route('/shows')
def shows():
    # displays list of shows at /shows
    shows = (
        db.session.query(Show, Venue, Artist)
        .join(Venue, Show.venue_id == Venue.id)
        .join(Artist, Show.artist_id == Artist.id)
        .order_by(Show.start_time)
        .all()
    )
    data = [
        {
            "venue_id": venue.id,
            "venue_name": venue.name,
            "artist_id": artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": show.start_time.isoformat(),
        }
        for show, venue, artist in shows
    ]
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    start_time_raw = request.form.get('start_time', '').strip()
    try:
        if "T" in start_time_raw:
            start_time = datetime.fromisoformat(start_time_raw)
        else:
            try:
                start_time = datetime.strptime(start_time_raw, "%Y-%m-%d %H:%M")
            except ValueError:
                start_time = datetime.strptime(start_time_raw, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        flash('An error occurred. Show could not be listed.')
        return render_template('pages/home.html')
    show = Show(
        artist_id=request.form['artist_id'],
        venue_id=request.form['venue_id'],
        start_time=start_time,
    )
    data = show
    try:
        db.session.add(show)
        db.session.commit()
    except Exception:
        db.session.rollback()
        flash('An error occurred. Show could not be listed.')
        return render_template('pages/home.html')

    # on successful db insert, flash success
    flash('Show was successfully listed!')
    return render_template('pages/home.html')
