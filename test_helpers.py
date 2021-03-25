import os
from unittest import TestCase
from models import db, connect_db, User, Boathouse
from helpers import Weather


os.environ['DATABASE_URL'] = 'postgresql:///rowable-test'

from app import app, CURR_USER_KEY


db.create_all()
app.config['WTF_CSRF_ENABLED'] = False
app.config['SECRET_KEY'] = 'fubar'


class HelpersTestCase(TestCase):
    """Tests for helpers.py"""
    def setUp(self):
        """Setup test client, add sample data"""
        self.client = app.test_client()
        Boathouse.query.delete()
        User.query.delete()
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
        self.wind_direction = 135
        self.wind_speed = 10
        self.conditions = 'Tornado'

    def tearDown(self):
        """Teardown session"""
        db.session.rollback()

    def test_get_weather(self):
        assert False

    def test_wind_dir(self):
        """Does return correct wind speed/direction?"""
        result = None, 10, 10, None
        maybe = Weather.wind_dir()
        self.assertEqual(result, maybe)

    def test_is_it_safe_conditions(self):
        result = 'Tornados predicted'
        maybe = Weather.is_it_safe_conditions()
        self.assertEqual(result, maybe)


    def test_is_it_safe_wind(self):
        assert False
