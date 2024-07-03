#!/usr/bin/env python3
"""A script that sets up a flask web app"""
from flask import Flask, render_template, request
from flask_babel import Babel


class Config:
    """Config settings for Babel"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """determines best language match"""
    if 'locale' in request.args:
        if request.args['locale'] in app.config['LANGUAGES']:
            return request.args['locale']
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index_page() -> str:
    """Returns the home page of the app"""
    return render_template('4-index.html')


if __name__ == "__main__":
    app.run()
