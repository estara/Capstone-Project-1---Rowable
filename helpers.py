from flask import Flask
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from secret import BaseConfig
from models import Boathouse, User
from datetime import datetime
import requests


app = Flask(__name__)
mail = Mail(app)
app.config['SECURITY_PASSWORD_SALT'] = BaseConfig.SECURITY_PASSWORD_SALT
weather_url = 'http://api.openweathermap.org/data/2.5/onecall?&exclude=minutely,alerts,daily&'


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)


def generate_confirmation_token(email):
    """Generate email confirmation token"""
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    """Confirm token from confirmation email"""
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=app.config['SECURITY_PASSWORD_SALT'], max_age=expiration)
    except:
        return False
    return email


def make_boathouse_list(user):
    """Make list of user's favorite boathouses"""
    user_boathouse_list = []
    for boathouse in user.boathouses:
        user_boathouse_list.append(Boathouse.query.get_or_404(boathouse))
    return user_boathouse_list


class Weather:
    """Weather data and functions for when user wants to row"""
    def __init__(self, day_time, boathouse_id, user_id=1):
        self.user = User.query.get_or_404(user_id)
        self.boathouse = Boathouse.query.get_or_404(boathouse_id)
        self.day_time = day_time
        self.get_weather()

    def get_weather(self):
        """Get weather data from API"""
        try:
            response = requests.get(f'{weather_url}lat={self.boathouse.lat}&lon={self.boathouse.lon}&units=imperial&appid={BaseConfig.weather_key}')
        except:
            return ConnectionError
        response_decoded = response.json()
        idx = self.get_hourly_record(response_decoded)
        self.time = response_decoded['hourly'][idx]['dt']
        self.temp = response_decoded['hourly'][idx]['temp']
        self.feels_like = response_decoded['hourly'][idx]['feels_like']
        self.humidity = response_decoded['hourly'][idx]['humidity']
        self.sunrise = datetime.utcfromtimestamp(int(response_decoded['current']['sunrise']))
        self.sunset = datetime.utcfromtimestamp(int(response_decoded['current']['sunset']))
        self.wind_speed = response_decoded['hourly'][idx]['wind_speed']
        self.wind_direction = response_decoded['hourly'][idx]['wind_deg']
        self.conditions = response_decoded['hourly'][idx]['weather'][0]['main']

    def wind_dir(self):
        """Translate wind direction in degrees"""
        print(self.wind_direction)
        nwind, ewind, swind, wwind = None, None, None, None
        if self.wind_direction > 326 or self.wind_direction < 56:
            nwind = self.wind_speed
        if self.wind_direction > 33 and self.wind_direction < 146:
            ewind = self.wind_speed
        if self.wind_direction > 123 and self.wind_direction < 236:
            swind = self.wind_speed
        if self.wind_direction > 213 and self.wind_direction < 326:
            wwind = self.wind_speed
        return nwind, ewind, swind, wwind

    def is_it_safe_conditions(self):
        """Will weather type be safe?"""
        print(self.conditions)
        if self.conditions == 'Thunderstorm':
            return 'Unlikely, thunderstorms forecasted.'
        if self.conditions == 'Snow':
            return 'Questionable, snow forecasted. Use best judgement'
        if self.conditions == 'Smoke':
            return 'Potential air quality problems. Check current AQI before rowing.'
        if self.conditions == 'Dust':
            return 'Potential air quality problems. Check current AQI before rowing.'
        if self.conditions == 'Fog':
            return 'Limited visibility likely. Use caution.'
        if self.conditions == 'Sand':
            return 'Potential air quality problems. Check current AQI before rowing.'
        if self.conditions == 'Ash':
            return 'Potential air quality problems. Check current AQI before rowing.'
        if self.conditions == 'Squall':
            return 'Unlikely, squalls forecasted.'
        if self.conditions == 'Tornado':
            return 'Tornados predicted.'
        return True

    def is_it_safe_wind(self):
        """Determine whether wind speeds/directions are within safety limits"""
        nwind, ewind, swind, wwind = self.wind_dir()
        print(nwind, ewind, swind, wwind)
        rowable = None
        if nwind is not None and self.boathouse.nmax <= nwind:
            rowable = False
        elif nwind is not None:
            rowable = True
        if swind is not None and self.boathouse.smax <= swind:
            rowable = False
        elif swind is not None and rowable is None or rowable:
            rowable = True
        if ewind and self.boathouse.emax <= ewind:
            rowable = False
        elif ewind is not None and rowable is None or rowable:
            rowable = True
        if wwind and self.boathouse.wmax <= wwind:
            rowable = False
        elif wwind is not None and rowable is None or rowable:
            rowable = True
        return rowable

    def light_level(self):
        if self.day_time < self.sunrise or self.day_time < self.sunset:
            return False
        else:
            return True

    def get_hourly_record(self, response):
        idx = 0
        for entry in response['hourly']:
            if str(self.day_time) == str(datetime.fromtimestamp(int(entry['dt']))):
                return idx
            idx += 1
