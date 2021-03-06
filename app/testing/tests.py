import os
import pytest
import unittest
import tempfile
from app import app
import sqlalchemy

class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_index_page(self):
        response = self.app.get('/index', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_null_page(self):
        response = self.app.get('/aaa', content_type='html/text')
        self.assertEqual(response.status_code, 404)

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)


    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login1(self):
        rv = self.login('admin', 'daw8dwa98adw9s0a')
        self.assertIn(b'Username not found', rv.data)

    def test_login2(self):
        rv = self.login('admin123', 'gre8eg97eg7eg8eg')
        self.assertIn(b'Invalid password', rv.data)

    def test_login3(self):
        rv = self.login('test123', 'goose1234')
        self.assertIn(b'Invalid password', rv.data)

    def test_login_logout1(self):
        rv = self.login('test123', 'goose123')
        self.assertIn(b'You are now logged in', rv.data)
        rv = self.logout()
        self.assertIn(b'You are now logged out', rv.data)

    def test_login_logout2(self):
        rv = self.login('admin123', 'admin123')
        self.assertIn(b'You are now logged in', rv.data)
        rv = self.logout()
        self.assertIn(b'You are now logged out', rv.data)


    def register(self, name, username, email, password):
        return self.app.post('/register', data=dict(
            name=name,
            username=username,
            email=email,
            password=password,
            confirm=password
        ), follow_redirects=True)

    def test_register1(self):
        response = self.app.get('/register', content_type='html/text')
        self.assertEqual(response.status_code, 200)

        rv = self.register('garry123', 'garry123', 'garry123@mail.ru', 'garry123')
        self.assertIn(b'You are now registered', rv.data)

    def test_register2(self):
        rv = self.register('lisa', 'lisa123', 'lisa123@mail.ru', 'lisa123')
        self.assertIn(b'Field must be between 7 and 30 characters long.', rv.data)

    def test_register3(self):
        rv = self.register('lisa123', 'lisa1', 'lisa123@mail.ru', 'lisa123')
        self.assertIn(b'Field must be between 7 and 20 characters long.', rv.data)

    def test_register4(self):
        rv = self.register('lisa123', 'lisa123', 'lisa123@mail', 'lisa123')
        self.assertIn(b'Invalid email address.', rv.data)

    def test_register5(self):
        rv = self.register('lisa123', 'lisa123', 'lisa123@mail', 'lisa1')
        self.assertIn(b'Field must be between 7 and 20 characters long.', rv.data)


    def test_client_page(self):
        response = self.app.get('/client/index', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_product_page(self):
        response = self.app.get('/product/index', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_sale_page(self):
        response = self.app.get('/sale/index', content_type='html/text')
        self.assertEqual(response.status_code, 200)


    def client_adding(self, fio, address, phone, email):
        return self.app.post('/client/add', data=dict(
            fio=fio,
            address=address,
            phone=phone,
            email=email,
        ), follow_redirects=True)

    def test_client_adding1(self):
        rv = self.client_adding('Brandon Rodriguez', '5465 Thornridge Cir', '072-625-1347', 'brandon.rodriguez@example.com')
        self.assertIn(b'Post added', rv.data)

    def test_client_adding2(self):
        rv = self.client_adding('Brandon Rodriguez', '5465 Thornridge Cir', '072-625-1347', 'brandon.rodriguez@example')
        self.assertIn(b'Invalid email address', rv.data)

    def test_client_adding3(self):
        rv = self.client_adding('Brandon Rodriguez', '5465 Thornridge Cir', '072-62', 'brandon.rodriguez@example.com')
        self.assertIn(b'Field must be between 7 and 30 characters long', rv.data)


    def product_adding(self, name, price, number):
        return self.app.post('/product/add', data=dict(
            name=name,
            price=price,
            number=number,
        ), follow_redirects=True)

    def test_product_adding1(self):
        rv = self.product_adding('Xiaomi DEM-F600', '30', '32')
        self.assertIn(b'Post added', rv.data)

    def test_product_adding2(self):
        rv = self.product_adding('Xiaomi DEM-F600', '0', '32')
        self.assertIn(b'Number must be between 1 and 10000', rv.data)

    def test_product_adding3(self):
        rv = self.product_adding('Xiaomi DEM-F600', '30', 'thousand')
        self.assertIn(b'Not a valid integer value', rv.data)

if __name__ == '__main__':
    unittest.main()