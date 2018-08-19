import fakeredis
import redis
import uuid
from collections import namedtuple
from flask import current_app


class DownloadService:
    def __init__(self, queue):
        self.queue = queue

    def request_download(self, album):
        if not album.purchased:
            raise AlbumNotPurchasedError('Cannot download an unpurchased album')
        pending_download = PendingDownload(str(uuid.uuid4()))
        self.queue.enqueue(self.process_download, pending_download)
        return pending_download

    @staticmethod
    def process_download(pending_download):
        # Don't actually care about doing any real work here
        return True


PendingDownload = namedtuple('PendingDownload', ['id'])


class AlbumNotPurchasedError(Exception):
    pass


class DownloadQueueFactory:
    @staticmethod
    def create():
        if current_app.config['REDIS_URL']:
            return redis.from_url(current_app.config['REDIS_URL'])
        else:
            return fakeredis.FakeStrictRedis()
