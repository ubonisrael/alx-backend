#!/usr/bin/env python3
"""A script that sets up a flask web app"""
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index_page() -> str:
    """Returns the home page of the app"""
    return render_template('0-index.html')


if __name__ == "__main__":
    app.run()
