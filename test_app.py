import os
from unittest import TestCase
from models import db, connect_db, User, Boathouse


os.environ['DATABASE_URL'] = 'postgresql:///rowable-test'

from app import app, CURR_USER_KEY


db.create_all()
app.config['WTF_CSRF_ENABLED'] = False
app.config['SECRET_KEY'] = 'fubar'


class AppTestCase(TestCase):
    """Tests for app.py"""
    def setUp(self):
        """Setup test client, add sample data"""
        Boathouse.query.delete()
        User.query.delete()
        self.client = app.test_client()
        self.testuser = User.signup('testuser', 'test@test.com', 'testuser')
        self.tu2 = User.signup('test2', 'test2@test.com', 'password')
        db.session.commit()
        self.testuser.id = 3985
        self.testboathouse = Boathouse(name='testboathouse', address='1 test', city='testcity', state='ts',
                                       zip=00000, lat=45.6206077, lon=-122.8072977,
                                       activated=True, nmax=10, smax=10, emax=10, wmax=10, fun_limit=10)
        self.testboathouse2 = Boathouse(name='testboathouse2', address='2 test', city='testcity2', state='t2',
                                        zip=00000, lat=45.6206077, lon=-122.8072977)
        db.session.add(self.testboathouse2)
        db.session.add(self.testboathouse)
        db.session.commit()
        self.testboathouse2 = Boathouse.query.filter_by(name='testboathouse2').one()

    def tearDown(self):
        """Teardown session"""
        db.session.rollback()

    # def test_add_user_to_g(self):
    #     assert False
    #
    #
    # def test_do_login(self):
    #     assert False
    #
    #
    # def test_do_logout(self):
    #     assert False

    def test_get_index(self):
        """Can get home page?"""
        with self.client as c:
            resp = c.get('/')
            html = resp.get_data(as_text=True)
            self.assertEqual(200, resp.status_code)
            self.assertIn('<h1>Welcome to Rowable!</h1>', html)

    # def test_post_index(self):
    #     with self.client as c:
    #         resp = c.post('/', data={'day_time': ?????, 'boathouse': 1}, follow_redirects=True)
    #         html = resp.get_data(as_text=True)
    #

    def test_about(self):
        """Can get about page?"""
        with self.client as c:
            resp = c.get('/about')
            html = resp.get_data(as_text=True)
            self.assertEqual(200, resp.status_code)
            self.assertIn('<p>Rowable was created as a pet project by Heather Johnson.</p>', html)

    def test_get_login(self):
        """Can get login page?"""
        with self.client as c:
            resp = c.get('/login')
            html = resp.get_data(as_text=True)
            self.assertEqual(200, resp.status_code)
            self.assertIn('<h1>Login</h1>', html)

    def test_post_login(self):
        """Can login?"""
        with self.client as c:
            resp = c.post('/login', data={'username': 'test2', 'password': 'password'}, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertIn('<h1>test2</h1>', html)

    def test_logout(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

    def test_get_add_user(self):
        """Can get new user page?"""
        with self.client as c:
            resp = c.get('/newuser')
            html = resp.get_data(as_text=True)
            self.assertEqual(200, resp.status_code)
            self.assertIn('<h1>Create new user</h1>', html)

    def test_post_add_user(self):
        """Can add new user?"""
        with self.client as c:
            resp = c.post('/newuser', data={'username': 'testuser3', 'password': 'testpass', 'email': 'test3@test.com'},
                          follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertIn('Please confirm your account!', html)
            self.assertIn('<p>You have not confirmed your account.', html)

    def test_get_user_details(self):
        """Can get user details?"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            resp = c.get(f'/userdetail/{self.testuser.id}')
            html = resp.get_data(as_text=True)
            self.assertEqual(200, resp.status_code)
            self.assertIn('<h3>My favorite boathouses</h3>', html)
            self.assertIn('<h1>testuser</h1>', html)

    def test_delete_user_no_login(self):
        """Does delete user fail without login?"""
        with self.client as c:
            resp = c.post(f'/userdetail/{self.testuser.id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertIn('Welcome to Rowable', html)

    def test_delete_user(self):
        """Can delete user?"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.tu2.id
            resp = c.post(f'/userdetail/{self.tu2.id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertIn('<h1>Create new user</h1>', html)

    def test_boathouse_list(self):
        """Can get boathouse list?"""
        with self.client as c:
            resp = c.get('/boathouselist')
            html = resp.get_data(as_text=True)
            self.assertEqual(200, resp.status_code)
            self.assertIn('<p>At this time we can only provide support for US boathouses.</p>', html)
            self.assertIn('">testboathouse</a></li>', html)

    def test_get_activate_boathouse_no_login(self):
        """Does fail if not logged in?"""
        with self.client as c:
            resp = c.get(f'/activateboathouse/{self.testboathouse2.id}', follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertIn('Rowable Login', html)

    def test_get_activate_boathouse(self):
        """Can get activate boathouse page?"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            resp = c.get(f'/activateboathouse/{self.testboathouse2.id}')
            html = resp.get_data(as_text=True)
            self.assertEqual(200, resp.status_code)
            self.assertIn('<h3>Please enter maximum safe wind speeds below.</h3>', html)
            self.assertIn('<h1>Activate testboathouse2</h1>', html)

    def test_post_activate_boathouse(self):
        """Can activate boathouse?"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            resp = c.post(f'/activateboathouse/{self.testboathouse2.id}',
                          data={'boathouse': 2, 'nmax': 5, 'smax': 5, 'wmax': 5, 'emax': 5,
                                'fun_limit': 4, 'notes': 'fizzbang'}, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(200, resp.status_code)
            self.assertIn('<p>fizzbang</p>', html)
            self.assertIn('<h1>testboathouse2</h1>', html)
            self.assertIn('<p>North to south: 5</p>', html)

    def test_boathouse_details(self):
        """Can get details about boathouse?"""
        with self.client as c:
            resp = c.get(f'/boathousedetail/{self.testboathouse.id}')
            html = resp.get_data(as_text=True)
            self.assertEqual(200, resp.status_code)
            self.assertIn('<p>Max safe winds in mph:</p>', html)
            self.assertIn('<h1>testboathouse</h1>', html)

    # def test_confirm_email(self):
    #     assert False
    #
    #
    # def test_unconfirmed(self):
    #     assert False
