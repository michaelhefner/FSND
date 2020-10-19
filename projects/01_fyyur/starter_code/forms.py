from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField
from wtforms.validators import DataRequired, AnyOf, URL
from enum import Enum

class Genre(Enum):    
    ALTERNATIVE = ('Alternative', 'Alternative')
    BLUES = ('Blues','Blues')
    CLASSICAL = ('Classical', 'Classical')
    COUNTRY = ('Country', 'Country')
    ELECTRONIC =  ('Electronic', 'Electronic')
    FOLK = ('Folk', 'Folk')
    FUNK = ('Funk', 'Funk')
    HIP_HOP = ('Hip-Hop', 'Hip-Hop')
    HEAVY_METAL = ('Heavy Metal', 'Heavy Metal')
    INSTRUMENTAL = ('Instrumental', 'Instrumental')
    JAZZ = ('Jazz', 'Jazz')
    MUSICAL_THEATRE = ('Musical Theatre', 'Musical Theatre')
    POP = ('Pop', 'Pop')
    PUNK = ('Punk', 'Punk')
    RANDB = ('R&B', 'R&B')
    REGGAE = ('Reggae', 'Reggae')
    ROCK_N_ROLL = ('Rock n Roll', 'Rock n Roll')
    SOUL = ('Soul', 'Soul')
    OTHER = ('Other', 'Other')

class Facebook(Enum):
    LINK=('facebook_link')

class ShowForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )
class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=[
            Genre.ALTERNATIVE.value,
            Genre.BLUES.value,
            Genre.CLASSICAL.value,
            Genre.COUNTRY.value,
            Genre.ELECTRONIC.value,
            Genre.FOLK.value,
            Genre.FUNK.value,
            Genre.HIP_HOP.value,
            Genre.HEAVY_METAL.value,
            Genre.INSTRUMENTAL.value,
            Genre.JAZZ.value,
            Genre.MUSICAL_THEATRE.value,
            Genre.POP.value,
            Genre.PUNK.value,
            Genre.RANDB.value,
            Genre.REGGAE.value,
            Genre.ROCK_N_ROLL.value,
            Genre.SOUL.value,
            Genre.OTHER.value
        ]
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )

class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    phone = StringField(
        # TODO implement validation logic for state
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=[
            Genre.ALTERNATIVE.value,
            Genre.BLUES.value,
            Genre.CLASSICAL.value,
            Genre.COUNTRY.value,
            Genre.ELECTRONIC.value,
            Genre.FOLK.value,
            Genre.FUNK.value,
            Genre.HIP_HOP.value,
            Genre.HEAVY_METAL.value,
            Genre.INSTRUMENTAL.value,
            Genre.JAZZ.value,
            Genre.MUSICAL_THEATRE.value,
            Genre.POP.value,
            Genre.PUNK.value,
            Genre.RANDB.value,
            Genre.REGGAE.value,
            Genre.ROCK_N_ROLL.value,
            Genre.SOUL.value,
            Genre.OTHER.value
        ]
    )
    facebook_link = StringField(
        Facebook.LINK.value, validators=[URL()]
    )

# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM
