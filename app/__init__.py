from flask import Flask

app = Flask(__name__)
app.secret_key = "secret123"

from app import views