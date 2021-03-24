"""Forms for Rowable app"""
from wtforms_components import DateRange
from wtforms.fields.html5 import DateTimeLocalField
from wtforms import SelectField, StringField, IntegerField, PasswordField
from wtforms.validators import InputRequired, Email, Optional, NumberRange, Length, EqualTo
from flask_wtf import FlaskForm
from models import User
from datetime import datetime, timedelta


class UserForm(FlaskForm):
    """Form for adding users"""
    username = StringField('Username', validators=[InputRequired(), Length(min=2)])
    email = StringField('Email', validators=[InputRequired(), Email(), Length(min=6)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
    confirm = PasswordField('Repeat password', validators=[InputRequired(), EqualTo('password',
                                                                                    message='Passwords must match.')])

    def validate(self):
        initial_validation = super(UserForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True


class BoathouseForm(FlaskForm):
    """Form for activating boathouse"""
    nmax = IntegerField('Max safe north to south wind', validators=[Optional(), NumberRange(min=2)])
    smax = IntegerField('Max safe south to north wind', validators=[Optional(), NumberRange(min=2)])
    emax = IntegerField('Max safe east to west wind', validators=[Optional(), NumberRange(min=2)])
    wmax = IntegerField('Max safe west to east wind', validators=[Optional(), NumberRange(min=2)])
    fun_limit = IntegerField('Max wind for rowing to be fun', validators=[Optional()])
    notes = StringField('Notes about rowing here', validators=[Optional()])


class LoginForm(FlaskForm):
    """Login form"""
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class EditUserForm(FlaskForm):
    """Form for editing user details"""
    c_or_f = SelectField('Preferred temperature units', choices=[('metric', 'Celsius'), ('imperial', 'Fahrenheit')])
    boathouses = SelectField(u'Add a favorite boathouse', coerce=int)


class RowableForm(FlaskForm):
    """Form for selecting day and time to get info for"""
    boathouse = SelectField(u'Boathouse you want to row from', coerce=int)
    day_time = DateTimeLocalField('Day and time you would like to row', format='%Y-%m-%dT%H:00', default=datetime.now(),
                                  validators=[InputRequired(), DateRange(min=datetime.now(),
                                                                         max=datetime.now() + timedelta(hours=48))])


