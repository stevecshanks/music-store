import json

from flask import Blueprint
from store.repositories import AlbumRepository

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/albums')
def albums():
    return json.dumps([{
        'id': album.id,
        'artist': album.artist,
        'name': album.name,
        'cover_image_url': album.cover_image_url,
        'bandcamp_url': album.bandcamp_url,
        'purchased': album.purchased,
        'rating': album.rating
    } for album in AlbumRepository.get_all()])
