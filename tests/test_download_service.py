import unittest
from store.models import Album
from store.services import DownloadService, AlbumNotPurchasedError


class TestDownloadService(unittest.TestCase):
    def test_unpurchased_albums_cannot_be_downloaded(self):
        album = Album()
        download_service = DownloadService()
        with self.assertRaises(AlbumNotPurchasedError):
            download_service.request_download(album)

    def test_download_requests_return_a_pending_download(self):
        album = Album(purchased=True)
        download_service = DownloadService()
        pending_download = download_service.request_download(album)
        self.assertIsNotNone(pending_download.id)
