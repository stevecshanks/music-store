import fakeredis
import random
import redis
import time
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
        self.queue.enqueue(process_download, pending_download)
        return pending_download


PendingDownload = namedtuple('PendingDownload', ['id'])


def process_download(pending_download):
    # Don't actually care about doing any real work here, but look like we are...
    time.sleep(random.randint(5, 10))
    return True


class AlbumNotPurchasedError(Exception):
    pass


class DownloadQueueFactory:
    @staticmethod
    def create():
        if current_app.config['REDIS_URL']:
            return redis.from_url(current_app.config['REDIS_URL'])
        else:
            return fakeredis.FakeStrictRedis()
