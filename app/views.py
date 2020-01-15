from flask import render_template, flash, redirect, Response, url_for, session, logging, request
from app import app
from app.forms import RegisterForm
from app.db_connection import connect_to_db
import hashlib


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title='Home')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = form.password.data

        conn, cursor, last_id = connect_to_db('usersDB', "select id from users")

        next_id = last_id + 1
        md5_pass = hashlib.md5(password.encode('utf-8')).hexdigest()
        SQLCommand = ("INSERT INTO users(id, name, username, email, password) VALUES (?,?,?,?,?)")
        values = [next_id, name, username, email, md5_pass]
        cursor.execute(SQLCommand, values)
        conn.commit()
        conn.close()

        flash('You are now registered', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_form = request.form['password']
        md5_pass = hashlib.md5(password_form.encode('utf-8')).hexdigest()

        conn, cursor, last_id = connect_to_db('usersDB', "select id from users")
        cursor.execute("SELECT * FROM users where username = ?", username)
        data = cursor.fetchone()

        if data != None:
            password = data[4]

            if password == md5_pass:

                flash('You are now logged in', 'success')
                return redirect(url_for('index'))
            else:
                error = "Invalid password"
                return render_template('login.html', error=error)
            cursor.close()
        else:
            error = "Username not found"
            return render_template('login.html', error=error)

    return render_template('login.html')