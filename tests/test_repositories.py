import unittest
import store
from store.repositories import AlbumRepository, AlbumNotFoundError
from store.models import db, Album


class TestAlbumRepository(unittest.TestCase):
    def setUp(self):
        app = store.create_app(test_config={'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
        app.app_context().push()
        db.create_all(app=app)

        self.album_1 = Album(id=1, artist='Test 1', name='Test 1', cover_image_url='', bandcamp_url='', purchased=True)
        self.album_2 = Album(id=2, artist='Test 2', name='Test 2', cover_image_url='', bandcamp_url='')

        db.session.add(self.album_1)
        db.session.add(self.album_2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()

    def test_album_can_be_retrieved_by_id(self):
        self.assertEqual(AlbumRepository.get_by_id(1), self.album_1)

    def test_error_raised_if_album_id_does_not_exist(self):
        with self.assertRaises(AlbumNotFoundError):
            AlbumRepository.get_by_id(99)

    def test_all_albums_can_be_retrieved(self):
        albums = AlbumRepository.get_all()
        self.assertEqual(len(albums), 2)
        self.assertTrue(self.album_1 in albums)
        self.assertTrue(self.album_2 in albums)

    def test_purchased_albums_can_be_retrieved(self):
        albums = AlbumRepository.get_purchased()
        self.assertEqual(albums, [self.album_1])

    def test_unpurchased_albums_can_be_retrieved(self):
        albums = AlbumRepository.get_unpurchased()
        self.assertEqual(albums, [self.album_2])