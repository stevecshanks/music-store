from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from store.models import Album

bp = Blueprint('albums', __name__, url_prefix='/albums')


@bp.route('/')
def index():
    albums = Album.query.all()

    return render_template('albums/index.html', albums=albums)
