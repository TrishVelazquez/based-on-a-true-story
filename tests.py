import unittest
import os
import flask
# from flask_testing import LiveServerTestCase
# from selenium import webdriver
from server import app
from model import db, User, Movie, Truth, Rating, example_data, connect_to_db, init_app

################################################################
# Route Tests #
################################################################

class ServerTests(unittest. TestCase):
    """Flask tests that test routes on the site"""

    def setUp(self):
        """Things to do before every test"""

        self.client = app.test_client()
        app.config['TESTING'] = True


    def test_homepage(self):
        """Test if homepage loads"""

        results = self.client.get("/")

        self.assertEqual(results.status_code, 200)
        self.assertIn(b"Based on a True Story", results.data)
        self.assertIn(b"Search for a movie that's based on a true story.", results.data)


    def test_login(self):
        """Test if login page loads"""

        results = self.client.get("/login")

        self.assertEqual(results.status_code, 200)
        self.assertIn(b"Welcome Back", results.data)
        self.assertIn(b"Email:", results.data)
        self.assertIn(b"Password:", results.data)


    def test_create_account(self):
        """Test if create account page loads"""

        results = self.client.get("/create-account")

        self.assertEqual(results.status_code, 200)
        self.assertIn(b"You belong here.", results.data)
        self.assertIn(b"Username:", results.data)
        self.assertIn(b"Email:", results.data)
        self.assertIn(b"Password:", results.data)



################################################################
# Database Tests #
################################################################

class DatabaseTestsNoAccount(unittest. TestCase):
    """Flask tests that use data from the database"""

    def setUp(self):
        """Things to do before every test"""

        self.client = app.test_client()
        app.config['TESTING'] = True
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()


    def test_process_account(self):
        """Test that a user can create an account"""

        results = self.client.post("/process-account",
                                data={'username': "flixter",
                                'email': "cat@yahoo.com",
                                'password': "cats"},
                                follow_redirects=True)

        self.assertEqual(results.status_code, 200)
        self.assertIn(b"Your account has been created!", results.data)
        self.assertIn(b"Please log in.", results.data)
        self.assertIn(b"Welcome Back", results.data)
        self.assertNotIn(b"You belong here", results.data)


    def test_create_account_username_taken(self):
        """Test redirect for existing username"""

        results = self.client.post("/process-account",
                                data={'username': "filmbuff",
                                'email': "myemail@yahoo.com",
                                'password': "pass"},
                                follow_redirects=True)

        self.assertEqual(results.status_code, 200)
        self.assertIn(b"That username is taken!", results.data)
        self.assertIn(b"Please try another.", results.data)
        self.assertIn(b"You belong here", results.data)
        self.assertNotIn(b"Your account has been created!", results.data)
        self.assertNotIn(b"Please login.", results.data)


    def test_create_account_account_exists(self):
        """Test redirect for existing user trying to make a new account"""

        results = self.client.post("/process-account",
                                data={'username': "newuser",
                                'email': "123@gmail.com",
                                'password': "somepassword"},
                                follow_redirects=True)
        
        self.assertEqual(results.status_code, 200)
        self.assertIn(b"Your email is already registerd.", results.data)
        self.assertIn(b"Please log in", results.data)
        self.assertIn(b"Welcome Back", results.data)
        self.assertNotIn(b"You belong here.", results.data)
        self.assertNotIn(b"Username:", results.data)


    def test_login(self):
        """Test is login is working"""

        results = self.client.post("/login-verify",
                                data={'email': "films@yahoo.com",
                                'password': "films"},
                                follow_redirects=True)
        
        self.assertEqual(results.status_code, 200)
        self.assertIn(b"Logged in.", results.data)
        self.assertIn(b"Click here to sign out.", results.data)
        self.assertNotIn(b"Click here to sign in.", results.data)
        self.assertNotIn(b"Click here to create an account.", results.data)


    def test_browse_movies(self):
        """Test if 'browse movies' page loads/displays"""

        results = self.client.get("/movie-list")

        self.assertEqual(results.status_code, 200)
        self.assertIn(b"Movies people are talking about.", results.data)


    def test_movie_display_no_account(self):
        """Test movie display for a user without a registered account"""

        results = self.client.get("/movies/1")

        self.assertEqual(results.status_code, 200)
        self.assertIn(b"Please log in to submit a Truth.", results.data)
        self.assertNotIn(b"What's your Truth?", results.data)

    def test_search_function_success(self):
        """Test the search bar with a successful search"""

        results = self.client.get("/search-results?query=blackkklansman")

        self.assertEqual(results.status_code, 200)
        self.assertIn(b"BlacKkKlansman", results.data)
        self.assertIn(b"Yeah, that movie is based on a true story!", results.data)
        self.assertNotIn(b"That movie isn't based on a true story.", results.data)


    def test_search_function_failure(self):
        """Test the search bar with a failed search"""

        results = self.client.get("/search-results?query=1q2w",
                                follow_redirects=True)

        self.assertEqual(results.status_code, 200)
        self.assertIn(b"Oops, that&#39;s not a movie title.", results.data)
        self.assertIn(b"Please try again.", results.data)
        self.assertNotIn(b"This movie matches your search:", results.data)


    def test_search_function_not_a_bio(self):
        """Test the search bar with a movie that is not a 'true' story"""

        results = self.client.get("/search-results?query=beetlejuice")

        self.assertEqual(results.status_code, 200)
        self.assertIn(b"Hmmmm.", results.data)
        self.assertIn(b"Want to search again?", results.data)
        self.assertNotIn(b"Yeah, that movie is based on a true story!", results.data)


    def tearDown(self):
        """Things to do after every test"""

        db.session.close()
        db.drop_all()
        db.engine.dispose()


################################################################
# Tests With Active Session #
################################################################

class FlaskTestsLoggedIn(unittest. TestCase):
    """Tests that run while user is logged in"""

    def setUp(self):
        """Things to do before every test"""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]
        self.client = app.test_client()
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()


        with self.client.session_transaction() as session:
            session['active_user'] = "filmbuff"
            session['active_user_id'] = 1


    def test_logout(self):
        """Test if logout works"""

        results = self.client.get("/logout",
                            follow_redirects=True)

        self.assertEqual(results.status_code, 200)
        self.assertIn(b"You&#39;ve been logged out.", results.data)
        self.assertIn(b"We&#39;ll miss you.", results.data)
        self.assertNotIn(b"Click here to sign out.", results.data)


    def test_movie_display_registered_account(self):
        """Test movie display for a user with a registered account"""

        results = self.client.get("movies/1")

        self.assertEqual(results.status_code, 200)
        self.assertIn(b"What's your Truth?", results.data)
        self.assertNotIn(b"Please log in to submit a Truth.", results.data)


    def test_add_truth(self):
            """Test that a registered user can add a truth to the database"""

            results = self.client.post("/movies/1",
                                    data={'title': "A Truth",
                                    'truth': "Some stuff",
                                    'resource': "www.stuff.com"},
                                    follow_redirects=True)

            self.assertEqual(results.status_code, 200)
            self.assertIn(b"See some Truth discussion:", results.data)
            self.assertIn(b"Your truth has been submitted!", results.data)
            self.assertNotIn(b"Boo! There are no truths here yet.", results.data)


    def tearDown(self):
        """Things to do after every test"""

        db.session.close()
        db.drop_all()
        db.engine.dispose()



################################################################
# Selenium Test WIP #
################################################################

# class TestBase(unittest. TestCase):

#     def setUp(self):
#         """Things to do before every test"""

#         self.browser = webdriver.Firefox()

#     def tearDown(self):

#         self.driver.quit()

#     def test_server_is_up_and_running(self):

#         self.browser.get('http://localhost:5000')
#         self.assertEqual(results.status_code, 200)
#         self.assertEqual(self.browser.title, 'Based on a true story')



################################################################
#
################################################################

if __name__ == "__main__":
    unittest.main()

    