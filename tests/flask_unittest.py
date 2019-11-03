from main import app
import os
import unittest
import random
from string import ascii_lowercase, digits
from flask import session

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

    # Test on button message
    def home_button_test(self):
        session['user_email'] = 'Test@email.com'

    # # Ensure articles works
    # def test_articles_page(self):
    #     tester = app.test_client(self)
    #     response = tester.get('/articles', content_type='html/text')
    #     self.assertTrue('Articles' in response.data)

    # # ensure login works
    # def test_login(self):
    #     tester = app.test_client(self)
    #     response = tester.post(
    #         '/login',
    #         data=dict(username="admin",password="admin"),
    #         follow_redirects=True
    #     )
    #     self.assertIn('You are now logged in', response.data)

    # # Ensure logout behaves correctly
    # def test_logout(self):
    #     tester = app.test_client(self)
    #     response = tester.post(
    #         '/login',
    #         data=dict(username="admin",password="admin"),
    #         follow_redirects=True
    #     )
    #     response = tester.get('/logout', follow_redirects=True)
    #     self.assertIn('You are now logged out', response.data)

    # # ensure dashboard works
    # def test_dash(self):
    #     tester = app.test_client(self)
    #     response = tester.post(
    #         '/login',
    #         data=dict(username="admin",password="admin"),
    #         follow_redirects=True
    #     )
    #     response = tester.get('/dashboard', content_type='html/text')
    #     self.assertIn('Dashboard', response.data)

    # # ensure add article works
    # def test_add_article(self):
    #     tester = app.test_client(self)
    #     response = tester.post(
    #         '/login',
    #         data=dict(username="admin",password="admin"),
    #         follow_redirects=True
    #     )
    #     response = tester.get('/dashboard', content_type='html/text')
    #     response = tester.get('/add_article', content_type='html/text')
    #     self.assertIn('Add Article', response.data)


    # ensure login via google works
    # Python unittests does not support external links
    # ensure login via facebook works
    # Python unittests does not support external links

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(FlaskTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)