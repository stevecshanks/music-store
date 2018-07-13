import unittest
from store.models import Album, AlbumAlreadyPurchasedError, InvalidRatingError


class TestAlbum(unittest.TestCase):
    def test_album_can_be_purchased(self):
        album = Album()
        album.purchase()
        self.assertTrue(album.purchased)

    def test_album_cannot_be_purchased_multiple_times(self):
        album = Album()
        album.purchase()
        with self.assertRaises(AlbumAlreadyPurchasedError):
            album.purchase()

    def test_album_can_be_rated(self):
        album = Album()
        album.rate(4)
        self.assertEqual(album.rating, 4)

    def test_album_rating_cannot_be_invalid(self):
        for invalid_rating in [0, 6, None]:
            with self.subTest(invalid_rating=invalid_rating):
                with self.assertRaises(InvalidRatingError):
                    album = Album()
                    album.rate(invalid_rating)