import os
import datetime
import pytz
from flask import Flask, render_template, session, flash, redirect, url_for, g
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, Boathouse, User
from forms import UserForm, BoathouseForm, LoginForm, EditUserForm, RowableForm
from helpers import Weather, send_email, generate_confirmation_token, confirm_token, add_to_list
from secret import BaseConfig


CURR_USER_KEY = "curr_user"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
app.config['WTF_CSRF_ENABLED'] = BaseConfig.WTF_CSRF_ENABLED
app.config['SECRET_KEY'] = BaseConfig.SECRET_KEY
connect_db(app)
db.create_all()


@app.before_request
def add_user_to_g():
    """If user is logged in, add curr user to Flask global."""
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None


def do_login(user):
    """Log in user."""
    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user"""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/', methods=['GET', 'POST'])
def index():
    """Display home page/process rowable form"""
    boathouse_choices = [(b.id, b.name) for b in Boathouse.query.filter_by(activated=True).order_by('name').all()]
    form = RowableForm()
    form.boathouse.choices = boathouse_choices
    if form.validate_on_submit():
        if not g.user:
            weather = Weather(form.day_time.data, form.boathouse.data)
        else:
            weather = Weather(form.day_time.data, form.boathouse.data, session[CURR_USER_KEY])

        conditions = weather.is_it_safe_conditions()
        wind = weather.is_it_safe_wind()
        light = weather.light_level()
        weather.c_or_f()

        if wind and light and conditions == True:
            success = 'You can row! Have fun.'
            return render_template('result.html', result=success, weather=weather)
        elif wind and light and conditions:
            return render_template('result.html', result=conditions, weather=weather)
        elif not light and wind and conditions == True:
            dark = 'Safe to row! It will be dark, make sure you have lights.'
            return render_template('result.html', result=dark, weather=weather)
        elif not light and wind and conditions:
            maybe_dark = f'{conditions}. It will be dark, make sure you have lights if you choose to row.'
            return render_template('result.html', result=maybe_dark, weather=weather)
        else:
            nope = "You probably shouldn't row."
            return render_template('result.html', result=nope, weather=weather)

    return render_template('index.html', form=form)


@app.route('/about')
def about():
    """Display about page"""
    return render_template('about.html')


#########################################################################################
# User routes


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
        if user:
            do_login(user)
            flash(f'Hello, {user.username}!', 'success')
            return redirect(f'userdetail/{user.id}')
        flash('Invalid credentials.', 'danger')
        return redirect('/login')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""
    do_logout()
    flash('Success logging out', 'success')
    return redirect('/')


@app.route('/newuser', methods=['GET', 'POST'])
def add_user():
    """Add new user"""
    form = UserForm()
    if form.validate_on_submit():
        try:
            user = User.signup(username=form.username.data, password=form.password.data, email=form.email.data)
        except IntegrityError:
            flash('Username already taken', 'danger')
            return render_template('/newuser', form=form)
        db.session.commit()
        token = generate_confirmation_token(user.email)
        confirm_url = url_for('confirm_email', token=token, _external=True)
        html = render_template('activate.html', confirm_url=confirm_url)
        subject = 'Please confirm your email'
        send_email(user.email, subject, html)
        return redirect("/unconfirmed")
    else:
        return render_template('newuser.html', form=form)


@app.route('/userdetail/<int:user_id>', methods=['GET', 'POST'])
def user_details(user_id):
    """Display/edit user details"""
    if not g.user or g.user.id != user_id:
        flash('Access unauthorized.', 'danger')
        return redirect("/login")
    boathouse_choices = [(b.id, b.name) for b in Boathouse.query.order_by('name')]
    form = EditUserForm()
    form.boathouses.choices = boathouse_choices
    user = User.query.get_or_404(user_id)
    if user.confirmed is False:
        flash('Please confirm your email account.', 'danger')
    if form.validate_on_submit():
        user.c_or_f = form.c_or_f.data
        user.boathouses = add_to_list(user.boathouses, form.boathouses.data)
        db.session.add(user)
        db.session.commit()
        print('updated boathouses ****************************')
        return redirect(f'/userdetail/{user_id}')
    if user.boathouses is not None:
        print('get boathouses ****************************')
        print(user.boathouses)
        boathouses = [b for b in Boathouse.query.filter(boathouse.id.in_(user.boathouses))]
        print('got boathouses ******************************')
    else:
        print('no boathouses *********************')
        boathouses = None
    return render_template('userdetail.html', form=form, user=user, boathouses=boathouses)


@app.route('/userdetail/<int:user_id>/delete')
def delete_user(user_id):
    """Delete user."""
    if not g.user or g.user.id != user_id:
        return redirect("/")
    user = User.query.get_or_404(user_id)
    do_logout()
    db.session.delete(user)
    db.session.commit()
    return redirect('/newuser')


#######################################################################################
# Boathouse routes


@app.route('/boathouselist')
def boathouse_list():
    """Display list of boathouses"""
    boathouses = Boathouse.query.order_by(Boathouse.name).all()
    return render_template('boathouselist.html', boathouses=boathouses)


@app.route('/activateboathouse/<int:boathouse_id>', methods=['GET', 'POST'])
def activate_boathouse(boathouse_id):
    """Activate boathouse by adding max wind speeds"""
    if not g.user:
        flash('Must be logged in to activate a boathouse.', 'danger')
        return redirect('/login')
    if g.user.confirmed is False:
        flash('Must confirm email to activate boathouse.', 'danger')
        return redirect('/unconfirmed')
    timezone_choices = [t for t in pytz.country_timezones['US']]
    form = BoathouseForm()
    form.timezone.choices = timezone_choices
    boathouse = Boathouse.query.get_or_404(boathouse_id)
    if form.validate_on_submit():
        boathouse.nmax = form.nmax.data
        boathouse.smax = form.smax.data
        boathouse.emax = form.emax.data
        boathouse.wmax = form.wmax.data
        boathouse.fun_limit = form.fun_limit.data
        boathouse.notes = form.notes.data
        boathouse.activated = True
        db.session.add(boathouse)
        db.session.commit()
        return redirect(f'/boathousedetail/{boathouse_id}')
    return render_template('addboathouse.html', form=form, boathouse=boathouse)


@app.route('/boathousedetail/<int:boathouse_id>')
def boathouse_details(boathouse_id):
    """Display boathouse details"""
    boathouse = Boathouse.query.get_or_404(boathouse_id)
    return render_template('boathousedetail.html', boathouse=boathouse)


#########################################################################################
# Account confirmation routes


@app.route('/confirm/<token>')
def confirm_email(token):
    """Confirm account email address"""
    try:
        email = confirm_token(token)
    except:
        info = 'The confirmation link is invalid or has expired.'
        return render_template('confirm.html', info=info)
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        info = 'Account already confirmed. Please login.'
        return render_template('confirm.html', info=info)
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        info = 'You have confirmed your account. Thanks!'
        return render_template('confirm.html', info=info)


@app.route('/unconfirmed')
def unconfirmed():
    """remind users to confirm account email"""
    if g.user:
        if g.user.confirmed:
            return redirect('/')
        flash('Please confirm your account!', 'warning')
        return render_template('unconfirmed.html')
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
