#!/usr/bin/env python3
"""A script that sets up a flask web app"""
from flask import Flask, render_template, request, g
from flask_babel import Babel
from typing import Dict, Union
import pytz


class Config:
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_CHOICE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(login_as) -> Union[Dict, None]:
    """returns a dict containing user info or None if not found"""
    return None if login_as is None else users.get(int(login_as))


@app.before_request
def before_request() -> None:
    """
    uses get_user to get user details before every request
    is processed
    """
    login_as = request.args.get('login_as', None)
    g.user = get_user(login_as)


@babel.timezoneselector
def get_timezone() -> str:
    """Retrieves the timezone for a web page.
    """
    timezone = request.args.get('timezone', '').strip()
    if not timezone and g.user:
        timezone = g.user['timezone']
    try:
        return pytz.timezone(timezone).zone
    except pytz.exceptions.UnknownTimeZoneError:
        return app.config['BABEL_DEFAULT_TIMEZONE']


@babel.localeselector
def get_locale() -> str:
    """determines best language match"""
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    if g.user and g.user['locale'] in app.config["LANGUAGES"]:
        return g.user['locale']
    header_locale = request.headers.get('locale', '')
    if header_locale in app.config["LANGUAGES"]:
        return header_locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index_page():
    """Returns the home page of the app"""
    return render_template('7-index.html')


if __name__ == "__main__":
    app.run()
