from flask import Flask, render_template, url_for, request,jsonify,redirect
from flaskwebgui import FlaskUI  # get the FlaskUI class
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import TextField, SubmitField, TextAreaField , FieldList , FormField ,SelectField,Form,IntegerField,StringField
from wtforms.validators import  Length, Email, Required
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from sqlite3 import Error
from glob import glob
import csv

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
##adding department and list
@app.route('/department')
def department():
    return render_template('department.html')
###adding employee and removing employee
@app.route('/Employee')
def Employee():
    return render_template('employe_maintence.html')
####leave and attendance
@app.route('/Leave')
def Leave():
    return render_template('leave.html')
###set working days
@app.route('/working_days')
def working_days():
    return  render_template('working_days.html')
##employee list
@app.route('/Employee_list')
def Employee_list():
    return render_template('employee_list.html')
##department list
@app.route('/Department_list')
def Department_list():
    return render_template('department_list.html')
##attendance
@app.route('/Attendance')
def Attendance():
    return render_template('attendance.html')
#####salary
@app.route('/salary')
def salary():
    return render_template('salary.html')
##employee salaries
@app.route('/Salaries')
def Salaries():
    return render_template('Salaries.html')
##user settings
@app.route('/settings')
def settings():
    return render_template('settings.html')
if __name__ == "__main__":
   app.run(debug=True, host='0.0.0.0', port=5000)
