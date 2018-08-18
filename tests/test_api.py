from tests import ApiTestCase
from flask import url_for
from store.models import db, Album


class TestAlbums(ApiTestCase):
    def test_empty_list_returned_if_no_albums_in_database(self):
        response = self.get(url_for('api.list_albums'))
        self.assertEqual(response.status_code, 200)
        self.assertResponseEqualsJson(response, [])

    def test_album_json_is_returned_correctly(self):
        album = self._create_test_album()
        response = self.get(url_for('api.list_albums'))
        self.assertEqual(response.status_code, 200)
        self.assertResponseEqualsJson(response, [self._expected_json(album)])

    def test_rating_non_existent_album_returns_correct_error(self):
        response = self.put(url_for('api.rate_album', album_id=999), data={'rating': 1})
        self.assertEqual(response.status_code, 404)
        self.assertResponseEqualsJson(response, {'error': 'No album found with id 999'})

    def test_invalid_rating_returns_correct_error(self):
        album = self._create_test_album()
        response = self.put(url_for('api.rate_album', album_id=album.id), data={'rating': 99})
        self.assertEqual(response.status_code, 400)
        self.assertResponseEqualsJson(response, {'error': 'Rating 99 is invalid'})

    def test_rating_an_album_correctly_returns_the_updated_album(self):
        album = self._create_test_album(rating=1)
        response = self.put(url_for('api.rate_album', album_id=album.id), data={'rating': 5})
        self.assertEqual(response.status_code, 200)
        self.assertResponseEqualsJson(response, self._expected_json(album, rating=5))

    def test_purchasing_non_existent_album_returns_correct_error(self):
        response = self.post(url_for('api.purchase_album', album_id=999))
        self.assertEqual(response.status_code, 404)
        self.assertResponseEqualsJson(response, {'error': 'No album found with id 999'})

    def test_purchasing_the_same_album_twice_returns_correct_error(self):
        album = self._create_test_album(purchased=True)
        response = self.post(url_for('api.purchase_album', album_id=album.id))
        self.assertEqual(response.status_code, 400)
        self.assertResponseEqualsJson(response, {'error': 'Album has already been purchased'})

    def test_purchasing_an_album_correctly_returns_the_updated_album(self):
        album = self._create_test_album()
        response = self.post(url_for('api.purchase_album', album_id=album.id))
        self.assertEqual(response.status_code, 200)
        self.assertResponseEqualsJson(response, self._expected_json(album, purchased=True))

    @staticmethod
    def _create_test_album(**overrides):
        defaults = {'artist': 'Test Artist', 'name': 'Test', 'cover_image_url': 'a url', 'bandcamp_url': 'another url'}
        album = Album(**defaults, **overrides)
        db.session.add(album)
        db.session.commit()

        return album

    @staticmethod
    def _expected_json(album, **expected_values):
        defaults = {'id': album.id, 'artist': album.artist, 'name': album.name,
                    'cover_image_url': album.cover_image_url, 'bandcamp_url': album.bandcamp_url,
                    'purchased': album.purchased, 'rating': album.rating}
        return {**defaults, **expected_values}
