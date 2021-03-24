import os
from unittest import TestCase
from models import db, connect_db, User, Boathouse


os.environ['DATABASE_URL'] = 'postgresql:///rowable-test'

from app import app, CURR_USER_KEY


db.create_all()
app.config['WTF_CSRF_ENABLED'] = False
app.config['SECRET_KEY'] = 'fubar'


class HelpersTestCase(TestCase):
    """Tests for helpers.py"""
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

    def test_get_weather():
        with self.client as c:


    def test_wind_dir():
        assert False


    def test_is_it_safe_conditions():
        assert False


    def test_is_it_safe_wind():
        assert False
