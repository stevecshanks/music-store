import fakeredis
import random
import redis
import time
import uuid
from collections import namedtuple
from flask import current_app
from flask_socketio import SocketIO


class DownloadService:
    def __init__(self, queue):
        self.queue = queue

    def request_download(self, album):
        if not album.purchased:
            raise AlbumNotPurchasedError('Cannot download an unpurchased album')
        pending_download = Download(str(uuid.uuid4()), album.bandcamp_url)
        self.queue.enqueue(process_download, pending_download)
        return pending_download


Download = namedtuple('Download', ['id', 'url'])


def process_download(download):
    # Don't actually care about doing any real work here, but look like we are...
    time.sleep(random.randint(5, 10))

    socketio = SocketIO(message_queue=current_app.config['REDIS_URL'])
    socketio.emit('download ready', {'id': download.id, 'url': download.url})

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
