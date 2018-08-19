import unittest
from store.models import Album
from store.services import DownloadService, AlbumNotPurchasedError, process_download
from unittest.mock import patch


@patch('rq.Queue', autospec=True)
class TestDownloadService(unittest.TestCase):
    def test_unpurchased_albums_cannot_be_downloaded(self, queue):
        album = Album()
        download_service = DownloadService(queue)
        with self.assertRaises(AlbumNotPurchasedError):
            download_service.request_download(album)

    def test_download_requests_return_a_pending_download(self, queue):
        album = Album(purchased=True)
        download_service = DownloadService(queue)
        pending_download = download_service.request_download(album)
        self.assertIsNotNone(pending_download.id)

    def test_download_requests_are_added_to_queue(self, queue):
        album = Album(purchased=True)
        download_service = DownloadService(queue)
        pending_download = download_service.request_download(album)
        queue.enqueue.assert_called_once_with(process_download, pending_download)
