import uuid
from collections import namedtuple


class DownloadService:
    def request_download(self, album):
        if not album.purchased:
            raise AlbumNotPurchasedError('Cannot download an unpurchased album')
        return PendingDownload(str(uuid.uuid4()))


PendingDownload = namedtuple('PendingDownload', ['id'])


class AlbumNotPurchasedError(Exception):
    pass
