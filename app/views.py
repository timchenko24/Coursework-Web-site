from flask import render_template, flash, redirect, Response, url_for, session, logging, request
from app import app
from app.forms import RegisterForm, ClientForm, ProductForm
from app.support import get_user_status
from app.db_connection import connect_to_db, get_df_from_db
import hashlib
import pandas as pd


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

        conn, cursor, last_id = connect_to_db('usersDB', 'id', "select id from users")

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

        conn, cursor, last_id = connect_to_db('usersDB', 'id', "select id from users")
        cursor.execute("SELECT * FROM users where username = ?", username)
        data = cursor.fetchone()

        if data != None:
            password = data[4]

            if password == md5_pass:
                session['logged_in'] = True
                session['username'] = username

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


@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('index'))


@app.route('/dashboard')
@get_user_status
def dashboard():
    return render_template('dashboard.html')


@app.route('/client/index')
def client_index():
    df = get_df_from_db('TestDB', 'select FIO, Address, Phone, [E-mail] from Client')
    df.columns = ['ФИО', 'Адрес', 'Телефон', 'E-mail']
    return render_template("client_table/index.html", tables=[df.to_html(classes='table table-bordered',
                                                                         border=0, index=False, justify='left')])


@app.route('/client/add', methods=['GET', 'POST'])
def client_add():
    form = ClientForm(request.form)

    if request.method == 'POST' and form.validate():
        fio = form.fio.data
        address = form.address.data
        phone = form.phone.data
        email = form.email.data

        conn, cursor, last_id = connect_to_db('TestDB', 'Client code', "select [Client code] from Client")

        next_id = last_id + 1
        SQLCommand = ("INSERT INTO Client([Client code], FIO, Address, Phone, [E-mail]) VALUES (?,?,?,?,?)")
        values = [next_id, fio, address, phone, email]
        cursor.execute(SQLCommand, values)
        conn.commit()
        conn.close()

        flash('Post added', 'success')
        return redirect(url_for('client_index'))
    return render_template('client_table/add.html', form=form)


@app.route('/product/index')
def product_index():
    df = get_df_from_db('TestDB', 'select Name, Price, Number from Product')
    df.columns = ['Наименование', 'Цена', 'Кол-во']
    return render_template("product_table/index.html", tables=[df.to_html(classes='table table-bordered',
                                                                         border=0, index=False, justify='left')])


@app.route('/product/add', methods=['GET', 'POST'])
def product_add():
    form = ProductForm(request.form)

    if request.method == 'POST' and form.validate():
        name = form.name.data
        price = form.price.data
        number = form.number.data

        conn, cursor, last_id = connect_to_db('TestDB', 'Product code', "select [Product code] from Product")

        next_id = last_id + 1
        SQLCommand = ("INSERT INTO Product([Product code], Name, Price, Number) VALUES (?,?,?,?)")
        values = [next_id, name, price, number]
        cursor.execute(SQLCommand, values)
        conn.commit()
        conn.close()

        flash('Post added', 'success')
        return redirect(url_for('product_index'))
    return render_template('product_table/add.html', form=form)


@app.route('/sale/index')
def sale_index():
    df_sale = get_df_from_db('TestDB', 'select [Product code], [Client code], [Sale date], [Delivery date], Number from Sale')
    df_client = get_df_from_db('TestDB', 'select [Client code], FIO from Client')
    df_product = get_df_from_db('TestDB', 'select [Product code], Name from Product')

    df_sale_client = pd.merge(df_sale, df_client, how='right', on='Client code').drop(labels=['Client code'], axis=1)
    df_result = pd.merge(df_sale_client, df_product, how='left', on='Product code').drop(labels=['Product code'], axis=1)
    df_result.columns = ['Дата продажи', 'Дата доставки', 'Кол-во', 'ФИО покупателя', 'Товар']
    return render_template("sale_table/index.html", tables=[df_result.to_html(classes='table table-bordered',
                                                                         border=0, index=False, justify='left')])