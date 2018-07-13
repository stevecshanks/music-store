from flask import Blueprint, render_template, redirect, url_for, flash, request
from store.models import db, AlbumAlreadyPurchasedError, InvalidRatingError
from store.repositories import AlbumRepository, AlbumNotFoundError

bp = Blueprint('albums', __name__, url_prefix='/albums')


@bp.route('/')
def index():
    return render_template('albums/index.html', albums=AlbumRepository.get_all())


@bp.route('/purchased')
def purchased():
    return render_template('albums/index.html', albums=AlbumRepository.get_purchased(), active_page='purchased')


@bp.route('/unpurchased')
def unpurchased():
    return render_template('albums/index.html', albums=AlbumRepository.get_unpurchased(), active_page='unpurchased')


@bp.route('/buy/<int:album_id>')
def buy(album_id):
    try:
        album = AlbumRepository.get_by_id(album_id)
        album.purchase()
        db.session.add(album)
        db.session.commit()
        flash('Album purchased successfully!', 'success')
        return redirect(url_for('albums.purchased'))
    except AlbumNotFoundError:
        flash('Album not found', 'danger')
    except AlbumAlreadyPurchasedError:
        flash('You already own this album', 'warning')

    return redirect(url_for('albums.index'))


@bp.route('/rate/<int:album_id>')
def rate(album_id):
    rating = request.args.get('rating', type=int)

    try:
        album = AlbumRepository.get_by_id(album_id)
        album.rate(rating)
        db.session.add(album)
        db.session.commit()
    except AlbumNotFoundError:
        flash('Album not found', 'danger')
    except InvalidRatingError:
        flash('Invalid rating', 'danger')

    return redirect(request.referrer)

