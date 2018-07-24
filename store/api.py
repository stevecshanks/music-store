import json

from flask import Blueprint, request
from store.models import db
from store.repositories import AlbumRepository

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/albums')
def albums():
    return json.dumps([album_to_dict(album) for album in AlbumRepository.get_all()])


@bp.route('/albums/<int:album_id>/buy')
def buy(album_id):
    album = AlbumRepository.get_by_id(album_id)
    album.purchase()
    db.session.add(album)
    db.session.commit()

    return json.dumps(album_to_dict(album))


@bp.route('/albums/<int:album_id>/rate', methods=['PUT'])
def rate(album_id):
    rating = request.json.get('rating')

    album = AlbumRepository.get_by_id(album_id)
    album.rate(rating)
    db.session.add(album)
    db.session.commit()

    return json.dumps(album_to_dict(album))


def album_to_dict(album):
    return {
        'id': album.id,
        'artist': album.artist,
        'name': album.name,
        'cover_image_url': album.cover_image_url,
        'bandcamp_url': album.bandcamp_url,
        'purchased': album.purchased,
        'rating': album.rating
    }
