from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from collections import namedtuple

bp = Blueprint('albums', __name__, url_prefix='/albums')


@bp.route('/')
def index():
    Album = namedtuple('Album', ['artist', 'name', 'cover_image_url'])
    albums = [
        Album('Deus Vermin', 'Monument To Decay', 'https://f4.bcbits.com/img/a1486857090_16.jpg'),
        Album('hvíldarlauss dauðr', 'Terrorforming', 'https://f4.bcbits.com/img/a0234421477_16.jpg'),
        Album('Vacivus', 'Rite of Ascension', 'https://f4.bcbits.com/img/a1747549551_16.jpg'),
        Album('Bròn', 'Ànrach', 'https://f4.bcbits.com/img/a2353430697_16.jpg'),
        Album('Plague Rider', 'Paroxysm', 'https://f4.bcbits.com/img/a1359105345_16.jpg'),
    ]
    return render_template('albums/index.html', albums=albums)
