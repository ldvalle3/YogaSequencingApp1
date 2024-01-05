from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sequencing.db'
app.config['SECRET_KEY'] = '54a1e3f43f06dba85aa820ea'
db = SQLAlchemy(app)

from sequences import routes
