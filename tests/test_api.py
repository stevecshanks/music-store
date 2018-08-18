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
        self.assertResponseEqualsJson(response, [
            {'id': 1, 'artist': 'Test Artist', 'name': 'Test', 'cover_image_url': 'a url',
             'bandcamp_url': 'another url', 'purchased': False, 'rating': album.id}])
