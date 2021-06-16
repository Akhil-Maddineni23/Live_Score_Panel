from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.config['SECRET_KEY'] = 'a8f528b394599ad1342ae33b841db2d9'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from flaskblog import routes