from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from collections import namedtuple

bp = Blueprint('albums', __name__, url_prefix='/albums')


@bp.route('/')
def index():
    Album = namedtuple('Album', ['artist', 'name', 'cover_image_url', 'bandcamp_url'])

    albums = [
        Album('Deus Vermin', 'Monument To Decay', 'https://f4.bcbits.com/img/a1486857090_16.jpg',
              'https://deusvermin.bandcamp.com/album/monument-to-decay'),
        Album('hvíldarlauss dauðr', 'Terrorforming', 'https://f4.bcbits.com/img/a0234421477_16.jpg',
              'https://hvildarlaussdaudr.bandcamp.com/album/terrorforming'),
        Album('Vacivus', 'Rite of Ascension', 'https://f4.bcbits.com/img/a1747549551_16.jpg',
              'https://vacivus.bandcamp.com/album/rite-of-ascension'),
        Album('Bròn', 'Ànrach', 'https://f4.bcbits.com/img/a2353430697_16.jpg',
              'https://bronmusic.bandcamp.com/album/nrach'),
        Album('Plague Rider', 'Paroxysm', 'https://f4.bcbits.com/img/a1359105345_16.jpg',
              'https://plaguerider.bandcamp.com/album/paroxysm'),
    ]

    return render_template('albums/index.html', albums=albums)
