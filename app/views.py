from flask import render_template, flash, redirect, Response, url_for, session, logging, request
from app import app


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title='Home')
