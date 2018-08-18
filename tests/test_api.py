import json
from tests import ApiTestCase
from flask import url_for
from store.models import db, Album


class AlbumsTest(ApiTestCase):
    def test_empty_list_returned_if_no_albums_in_database(self):
        response = self.client.get(url_for('api.albums'))
        self.assertEqual(response.status_code, 200)
        self.assertResponseEqualsJson(response, [])

    def test_album_json_is_returned_correctly(self):
        album = Album(artist='Test Artist', name='Test', cover_image_url='a url', bandcamp_url='another url', rating=1)
        db.session.add(album)
        db.session.commit()

        response = self.client.get(url_for('api.albums'))
        self.assertEqual(response.status_code, 200)
        self.assertResponseEqualsJson(response,
                                      [{'id': album.id, 'artist': 'Test Artist', 'name': 'Test',
                                        'cover_image_url': 'a url', 'bandcamp_url': 'another url', 'purchased': False,
                                        'rating': 1}])

    def test_rating_non_existent_album_returns_correct_error(self):
        response = self.client.put(url_for('api.rate', album_id=999), data=json.dumps({'rating': 1}),
                                   headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 500)
        self.assertResponseEqualsJson(response, {'error': 'No album found with id 999'})

    def test_rating_an_album_correctly_returns_the_updated_album(self):
        album = Album(artist='Test Artist', name='Test', cover_image_url='a url', bandcamp_url='another url', rating=1)
        db.session.add(album)
        db.session.commit()

        response = self.client.put(url_for('api.rate', album_id=album.id), data=json.dumps({'rating': 5}),
                                   headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 200)
        self.assertResponseEqualsJson(response,
                                      {'id': album.id, 'artist': 'Test Artist', 'name': 'Test',
                                       'cover_image_url': 'a url', 'bandcamp_url': 'another url', 'purchased': False,
                                       'rating': 5})

    def test_purchasing_non_existent_album_returns_correct_error(self):
        response = self.client.get(url_for('api.buy', album_id=999))
        self.assertEqual(response.status_code, 500)
        self.assertResponseEqualsJson(response, {'error': 'No album found with id 999'})

    def test_purchasing_an_album_correctly_returns_the_updated_album(self):
        album = Album(artist='Test Artist', name='Test', cover_image_url='a url', bandcamp_url='another url')
        db.session.add(album)
        db.session.commit()

        response = self.client.get(url_for('api.buy', album_id=album.id))
        self.assertEqual(response.status_code, 200)
        self.assertResponseEqualsJson(response,
                                      {'id': album.id, 'artist': 'Test Artist', 'name': 'Test',
                                       'cover_image_url': 'a url', 'bandcamp_url': 'another url', 'purchased': True,
                                       'rating': None})

