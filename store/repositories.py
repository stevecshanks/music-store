from store.models import Album


class AlbumRepository:
    @staticmethod
    def get_by_id(album_id):
        album = Album.query.get(album_id)
        if not album:
            raise AlbumNotFoundError(f"No album found with id {album_id}")
        return album

    @staticmethod
    def get_all():
        return Album.query.all()


class AlbumNotFoundError(Exception):
    pass
