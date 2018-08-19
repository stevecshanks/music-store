import json
from rq import Connection, Queue

from flask import Blueprint, request, Response

from store.models import db, InvalidRatingError, AlbumAlreadyPurchasedError
from store.repositories import AlbumRepository, AlbumNotFoundError
from store.services import DownloadService, AlbumNotPurchasedError, DownloadQueueFactory


bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/albums')
def list_albums():
    return json.dumps([album_to_dict(album) for album in AlbumRepository.get_all()])


@bp.route('/albums/<int:album_id>/purchase', methods=['POST'])
def purchase_album(album_id):
    try:
        album = AlbumRepository.get_by_id(album_id)
        album.purchase()
        db.session.add(album)
        db.session.commit()

        return json.dumps(album_to_dict(album))
    except AlbumNotFoundError as e:
        return error_response(e, 404)
    except AlbumAlreadyPurchasedError as e:
        return error_response(e, 400)


@bp.route('/albums/<int:album_id>/rating', methods=['PUT'])
def rate_album(album_id):
    try:
        rating = request.json.get('rating')

        album = AlbumRepository.get_by_id(album_id)
        album.rate(rating)
        db.session.add(album)
        db.session.commit()
    except AlbumNotFoundError as e:
        return error_response(e, 404)
    except InvalidRatingError as e:
        return error_response(e, 400)

    return json.dumps(album_to_dict(album))


@bp.route('/albums/<int:album_id>/downloads', methods=['POST'])
def download_album(album_id):
    try:
        album = AlbumRepository.get_by_id(album_id)
        with Connection(DownloadQueueFactory.create()):
            download_service = DownloadService(Queue())
            pending_download = download_service.request_download(album)
            return json.dumps({'id': pending_download.id})
    except AlbumNotFoundError as e:
        return error_response(e, 404)
    except AlbumNotPurchasedError as e:
        return error_response(e, 400)


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


def error_response(exception, status_code):
    return Response(json.dumps({'error': str(exception)}), status_code)
