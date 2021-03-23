from flask import Flask, request
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from secret import BaseConfig
from models import Boathouse, User


app = Flask(__name__)
mail = Mail(app)
weather_url = 'http://api.openweathermap.org/data/2.5/onecall?&exclude=minutely,alerts,daily'


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=app.config['SECURITY_PASSWORD_SALT'], max_age=expiration)
    except:
        return False
    return email


class Weather:
    """Weather data and functions for when user wants to row"""
    def __init__(self, day_time, boathouse_id, user_id=1):
        self.user = User.query.get_or_404(user_id)
        self.boathouse = Boathouse.query.get_or_404(boathouse_id)
        self.day_time = day_time
        self.get_weather()
        self.convert_time()

    def get_weather(self):
        """Get weather data from API"""
        response = request.get(f'{weather_url}lat={self.boathouse.lat}&lon={self.boathouse.lon}&units={self.user.c_or_f}&appid={BaseConfig.weather_key}')
        self.time = response.hourly.dt
        self.temp = response.hourly.temp
        self.feels_like = response.hourly.feels_like
        self.humidity = response.hourly.humidity
        self.rain_prob = response.hourly.pop
        self.sunrise = response.current.sunrise
        self.sunset = response.current.sunset
        self.wind_speed = response.hourly.wind_speed
        self.wind_direction = response.hourly.wind_deg
        self.conditions = response.hourly.weather.main

    def wind_dir(self):
        """Translate wind direction in degrees"""
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
        rowable = None
        if nwind and self.boathouse.nmax > nwind:
            rowable = False
        elif nwind:
            rowable = True
        if swind and self.boathouse.smax > swind:
            rowable = False
        elif swind and rowable is None or rowable:
            rowable = True
        if ewind and self.boathouse.emax > ewind:
            rowable = False
        elif ewind and rowable is None or rowable:
            rowable = True
        if wwind and self.boathouse.wmax > wwind:
            rowable = False
        elif wwind and rowable is None or rowable:
            rowable = True
        return rowable

    def light_level(self):
        if self.day_time < self.sunrise or self.day_time > self.sunset:
            return False
        else:
            return True

    def convert_time(self):
        self.day_time = self.day_time.strftime('%s')
