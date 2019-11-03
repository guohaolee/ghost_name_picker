from main import app
import os
import unittest
import random
import json
from string import ascii_lowercase, digits
from flask import session

from lib.google_auth import is_logged_in

from fireo.models import Model
from fireo.fields import TextField, NumberField, IDField, DateTime

"""
   need to export the project path first
   Example: export PYTHONPATH=$PYTHONPATH:/Users/dereklee/Desktop/phq/ghost_name_picker
"""
class TestDB(Model):
    id = IDField()
    name = TextField()
    class_name = 'test_users'

    class Meta:
        collection_name = 'test_users'

    @classmethod
    def delete(cls, id):
        try:
            cls.collection.delete(f"{cls.class_name}/{id}")
            return True
        except Exception as e:
            return False

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        """ Setup unit testing env """
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        os.environ['AUTH_REDIRECT_URI'] = 'http://localhost:5000'

        self.name = ''.join(random.choice(ascii_lowercase) for v in range(12))
        self.id = ''.join(random.choice(digits) for v in range(12))
        user = TestDB()
        user.name = self.name
        user.id = self.id
        user.save()

        self.tester = app.test_client(self)
        self.assertEqual(app.testing, True)

    def tearDown(self):
        """ Tear down unit testing env """
        TestDB.delete(self.id)
        super().tearDown()

    # Ensure that Flask was set up correctly
    def test_index_page(self):
        response = self.tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure page 404 works
    def test_404_page(self):
        response = self.tester.get('/404', content_type='html/text')
        self.assertEqual(response.status_code, 404)

    # Test db
    def test_db(self):
        result = TestDB.collection.filter('name', '==', self.name).get()
        self.assertEqual(result.name, self.name)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(FlaskTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)