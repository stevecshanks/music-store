import json
import store
import unittest
from store.models import db


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = store.create_app(test_config={
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'SERVER_NAME': '{rv}.localdomain',
            'REDIS_URL': None,
        })
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


class ApiTestCase(AppTestCase):
    def setUp(self):
        super().setUp()
        self.client = self.app.test_client()

    def assertResponseEqualsJson(self, response, expected):
        self.assertEqual(self.response_as_json(response), expected)

    @staticmethod
    def response_as_json(response):
        return json.loads(response.get_data(as_text=True))

    def get(self, url):
        return self.client.get(url)

    def put(self, url, data=None):
        return self.client.put(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})

    def post(self, url, data=None):
        return self.client.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
