#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
app.config['DEBUG'] = True

migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column("genres", db.ARRAY(db.String(120)))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))
    website = db.Column(db.String(50))


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column("genres", db.ARRAY(db.String(120)))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(50))
    seeking_venue = db.Column(db.Boolean)


class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
    start_time = db.Column(db.DateTime)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime


#----------------------------------------------------------------------------#
# Functions.
#----------------------------------------------------------------------------#

def getUpcomingShowsForVenue(shows):
    upcomingShows = []
    for show in shows:
        if show.start_time > datetime.now():
            upcomingShows.append({
                "artist_id": show.artist_id,
                "artist_name": Artist.query.filter_by(id=show.artist_id).first().name,
                "artist_image_link": Artist.query.filter_by(id=show.artist_id).first().image_link,
                "start_time": str(show.start_time)
            })
    return upcomingShows


def getPastShowsForVenue(shows):
    pastShows = []
    for show in shows:
        if show.start_time < datetime.now():
            pastShows.append({
                "artist_id": show.artist_id,
                "artist_name": Artist.query.filter_by(id=show.artist_id).first().name,
                "artist_image_link": Artist.query.filter_by(id=show.artist_id).first().image_link,
                "start_time": str(show.start_time)
            })
    return pastShows


def getPastShowsForArtist(shows):
    pastShows = []
    for show in shows:
        if show.start_time < datetime.now():
            pastShows.append({
                "venue_id": show.venue_id,
                "venue_name": Venue.query.filter_by(id=show.venue_id).first().name,
                "venue_image_link": Venue.query.filter_by(id=show.venue_id).first().image_link,
                "start_time": str(show.start_time)
            })
    return pastShows


def getUpcomingShowsForArtist(shows):
    upcomingShows = []
    for show in shows:
        if show.start_time > datetime.now():
            upcomingShows.append({
                "venue_id": show.venue_id,
                "venue_name": Venue.query.filter_by(id=show.venue_id).first().name,
                "venue_image_link": Venue.query.filter_by(id=show.venue_id).first().image_link,
                "start_time": str(show.start_time)
            })
    return upcomingShows


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    data = []
    venues = Venue.query.all()
    venueLocation = set()
    for venue in venues:
        venueLocation.add((venue.city, venue.state))

    for location in venueLocation:
        data.append({
            "city": location[0],
            "state": location[1],
            "venues": []
        })
    for venue in venues:
        numShowsUpcoming = 0

        shows = Show.query.filter_by(venue_id=venue.id).all()

    for show in shows:
        if show.start_time > datetime.now():
            numShowsUpcoming += 1

    for entry in data:
        if venue.city == entry['city'] and venue.state == entry['state']:
            entry['venues'].append({
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": numShowsUpcoming
            })
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    searchTerm = request.form.get('search_term', '')
    venues = Venue.query.filter(Venue.name.ilike('%' + searchTerm + '%')).all()
    data = []

    for venue in venues:
        data.append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": 0
        })
    response = {
        "count": len(venues),
        "data": data
    }
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)
    shows = Show.query.filter_by(venue_id=venue_id)

    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": getPastShowsForVenue(shows),
        "upcoming_shows": getUpcomingShowsForVenue(shows),
        "past_shows_count": len(getPastShowsForVenue(shows)),
        "upcoming_shows_count": len(getUpcomingShowsForVenue(shows))
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
    form = VenueForm()
    try:
        print(form.name.data)
        venue = Venue(
            name=form.name.data,
            city=form.city.data,
            state=form.state.data,
            address=form.address.data,
            phone=form.phone.data,
            genres=form.genres.data,
            facebook_link=form.facebook_link.data,
            image_link="",
            seeking_talent=True,
            seeking_description="",
            website="")
        print('go')
        db.session.add(venue)
        db.session.commit()
        print('success')
        flash('Venue ' + form.name.data + ' was successfully listed!')
    except:
        flash('An error occurred. Venue ' +
              form['name'] + ' could not be listed')
        print('failed')
        db.session.rollback()
    finally:
        db.session.close()
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        venue = Venue.query.get(venue_id)
        db.session.delete(venue)
        db.session.commit()
        flash('Venue' + venue.venue_id + ' was successfully deleted.')
    except:
        flash('Venue' + venue.venue_id + ' was not deleted.')
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('venues'))

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    artists = Artist.query.all()
    data = []
    for artist in Artist.query.all():
        data.append({
            "id": artist.id,
            "name": artist.name,
            "num_upcoming_shows": 0

        })
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    searchTerm = request.form.get('search_term', '')
    artists = Artist.query.filter(Artist.name.ilike('%' + searchTerm + '%'))
    data = []
    for artist in artists:
        data.append({
            "id": artist.id,
            "name": artist.name,
            "num_upcoming_shows": 0
        })
    response = {
        "count": len(artists),
        "data": data
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.filter_by(id=artist_id).first()
    shows = Show.query.filter_by(artist_id=artist_id).all()

    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "image_link": artist.image_link,
        "past_shows": getPastShowsForArtist(shows),
        "upcoming_shows": getUpcomingShowsForArtist(shows),
        "past_shows_count": len(getPastShowsForArtist(shows)),
        "upcoming_shows_count": len(getUpcomingShowsForArtist(shows))
    }
    print(data)
    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.filter_by(id=artist_id).first()

    artist = {
        "id": artist_id,
        "name": artist.name,
        "genres": artist.genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_talent,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link

    }
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    try:
        form = ArtistForm()
        artist = Artist.query.filter_by(id=artist_id).first()

        artist = {
            "name": form.name.data,
            "genres": form.genres.data,
            "city": form.city.data,
            "state": form.state.data,
            "phone": form.phone.data,
            "website": "",
            "facebook_link": form.facebook_link.data,
            "seeking_venue": False,
            "seeking_description": "",
            "image_link": ""
        }

        db.session.commit()
        flash("Artist " + form.name + " was updated successfully.")
    except:
        db.session.rollback()
        flash("Artist " + form.name + " was not updated.")
    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = venue.query.filter_by(id=venue_id).first()

    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link
    }
    return render_template('forms/edit_venue.html', form=form, venue=data)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    try:
        form = VenueForm()
        venue = Venue.query.filter_by(id=venue_id).first()

        venue = {
            "name": form.name.data,
            "genres": form.genres.data,
            "address": form.address.data,
            "city": form.city.data,
            "state": form.state.data,
            "phone": form.phone.data,
            "website": "",
            "facebook_link": form.facebook_link.data,
            "seeking_venue": True,
            "seeking_description": "",
            "image_link": ""
        }
        db.session.commit()
        flash("Venue " + form.name.data + " was updated successfully.")
    except:
        db.session.rollback()
        flash("Venue " + form.name.data + " was not updated.")
    finally:
        db.session.close()

    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm()
    try:
        print("ready")
        
        artist = Artist(
            name=form.name.data,
            city=form.city.data,
            state=form.state.data,
            phone=form.phone.data,
            genres=form.genres.data,
            website="",
            facebook_link=form.facebook_link.data,
            seeking_venue=False,
            image_link=""
        )
        print(artist)

        print("after")
        db.session.add(artist)
        db.session.commit()
        flash("Artist " + form.name.data + " was created successfully.")
    except:
        db.session.rollback()
        flash("Artist " + form.name.data + " was not created.")
    finally:
        db.session.close()

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    data = []
    shows = Show.query.all()
    for show in shows:
        data.append({
            "venue_id": show.venue_id,
            "venue_name": Venue.query.filter_by(id=show.venue_id).first().name,
            "artist_id": show.artist_id,
        "artist_name": Artist.query.filter_by(id=show.artist_id).first().name,
        "artist_image_link": Artist.query.filter_by(id=show.artist_id).first().image_link,
        "start_time": str(show.start_time)
        })
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    form = ShowForm()
    try:
        print('ready set')
        show = Show(
            artist_id=form.artist_id.data,
            venue_id=form.venue_id.data,
            start_time=form.start_time.data)
        print('go')
        db.session.add(show)
        db.session.commit()
        print('success')
        flash('Venue ' + form.artist_id +
              ' was successfully listed!')
    except:
        flash('An error occurred. Venue ' +
              form.artist_id + ' could not be listed')
        print('failed')
        db.session.rollback()
    finally:
        db.session.close()
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
