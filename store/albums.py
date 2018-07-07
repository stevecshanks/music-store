from flask import Blueprint, render_template, redirect, url_for
from store.models import Album, db

bp = Blueprint('albums', __name__, url_prefix='/albums')


@bp.route('/')
def index():
    albums = Album.query.all()
    return render_template('albums/index.html', albums=albums)


@bp.route('/buy/<int:album_id>')
def buy(album_id):
    album = Album.query.get(album_id)
    if not album:
        raise ValueError('Album not found')
    if album.purchased:
        raise ValueError('You already own this album')

    album.purchased = True
    db.session.add(album)
    db.session.commit()

    return redirect(url_for('albums.index'))