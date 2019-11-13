from flask import Flask, render_template, url_for, request,jsonify
from flaskwebgui import FlaskUI  # get the FlaskUI class
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import TextField, SubmitField, TextAreaField , FieldList , FormField ,SelectField,Form,IntegerField,StringField
from wtforms.validators import  Length, Email, Required
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from sqlite3 import Error
from glob import glob

app = Flask(__name__,static_url_path='/static')
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
Bootstrap(app)
# Feed it the flask app instance (check bellow what param you can add)
ui = FlaskUI(app)
# do your logic as usual in Flask
@app.route("/",methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route("/biodata",methods=['GET','POST'])
def biodata():
	return render_template('biodata.html')

@app.route("/job",methods=['GET','POST'])
def job():
	return render_template('job.html')
	
@app.route("/hr",methods=['GET','POST'])
def hr():
	return render_template('employe_maintence.html')
ui.run()