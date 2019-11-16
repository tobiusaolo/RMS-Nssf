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

con = None
app = Flask(__name__)
Bootstrap(app)
# Feed it the flask app instance (check bellow what param you can add)
ui = FlaskUI(app)
#creating a connection to the database
def getConnection():
    databaseFile="Registration.db"
    global con
    if con == None:
        con=sqlite3.connect(databaseFile)
    return con

# do your logic as usual in Flask
@app.route("/index",methods=['GET','POST'])
def index():
    db=getConnection()
    c=db.cursor()
    result = c.execute("SELECT name From sqlite_master where type='table';").fetchall()
    table_names=sorted(list(zip(*result))[0])
    return render_template('admin_dashboard.html',table_names=table_names)

@app.route("/table_form",methods=['GET','POST'])
def table_form():
    return render_template('create_table.html')

@app.route('/submitdata',methods=['POST','GET'])
def submitdata():
    if request.method=='POST':
        columns=()
        table_name=request.form['table_name']
        text=request.form['text']
        columns=text
        db=getConnection()
        c=db.cursor()
        try:
            c.execute('CREATE TABLE {tn} ({fn})'.format(tn=table_name,fn=columns)) 
            return redirect(url_for('index'))
        except Exception as e:
            raise e

@app.route('/structure',methods=['POST','GET'])
def structure():
    db=getConnection()
    c=db.cursor()
    if request.method=='POST':
        tab_name=request.form['table_name']
        result = c.execute("PRAGMA table_info('%s')" % tab_name).fetchall()
    return render_template('dynamic.html',table_columns=result,tab_name=tab_name)


@app.route('/create_field',methods=['POST','GET'])
def create_field():
    if request.method=='POST':
        tab_name = request.form['table_name']
        field_name= request.form['field_name']
        data_type=request.form['Type']

        db=getConnection()
        c=db.cursor()
        try:
            c.execute("alter table {tn} add {cn} {dt}".format(tn=tab_name,cn=field_name,dt=data_type))
            con.commit()
            result = c.execute("PRAGMA table_info('%s')" % tab_name).fetchall()
            return render_template('dynamic.html',table_columns=result)
        except Exception as e:
            raise e
@app.route('/formdisplay',methods=['POST','GET'])
def formdisplay():
    if request.method=='POST':
        table_name=request.form['table_name']
        db=getConnection()
        c=db.cursor()
        cursor = c.execute('select * from {tn}'.format(tn=table_name))
        colnames=cursor.description
    return render_template('client.html',data_rows=colnames,table_name=table_name)

@app.route('/insert_record',methods=['POST','GET'])
def insert_record():
    db=getConnection()
    c=db.cursor()
    data=[]
    if request.method=='POST':
        for v in request.form:
            data.append(request.form[v])
            table_name=data[0]
            table_values=tuple(data[1:])
        try:
            cursor = c.execute('select () from {tn}'.format(tn=table_name))
            colnames=cursor.description
            fields=[]
            for field_name in colnames:
                fields.append(field_name[0])
            final_fields=tuple(fields)
            c.execute("Insert INTO {tn} {tbc} VALUES {tbv}".format(tn=table_name,tbc=final_fields,tbv=table_values))
            con.commit()
             # con.close()
        except sqlite3.IntegrityError:
            print('failed')
        return redirect(url_for('index'))

@app.route('/show',methods=['POST','GET'])
def show():
    global table_name
    if request.method=='POST':
        table_name=request.form['table_name']
        db=getConnection()
        c=db.cursor()
        try:
            result = c.execute('select * from {tn}'.format(tn=table_name))
            colnames=result.description
            cur=c.execute("select {col1},{col2},{col3},{col4},{col5},{col6},{col7} from {tn}".format(tn=table_name,col1="FIRSTNAME",col2="SURNAME",col3="NSSF_NUMBER",col4="STAFF_NUMBER",col5="BANK_NAME",col6="BANK_NUMBER",col7="POSITION_OR_TITLE"))
            rows = cur.fetchall()
            return render_template('original.html',rows=rows,table_name=table_name ,colnames=colnames)
        except Exception as e:
            raise e

@app.route('/showuser',methods=['POST','GET'])
def showuser():
    global table_name
    # if request.method=='POST':
    #     table_name=request.form['table_name']
    db=getConnection()
    c=db.cursor()
    try:
        # result = c.execute('select * from {tn}'.format(tn=tb))
        # colnames=result.description
        cur=c.execute("select {col1},{col2},{col3},{col4},{col5},{col6},{col7} from {tn}".format(tn="EmployeeRegistration",col1="FIRSTNAME",col2="SURNAME",col3="NSSF_NUMBER",col4="STAFF_NUMBER",col5="BANK_NAME",col6="BANK_NUMBER",col7="POSITION_OR_TITLE"))
        rows = cur.fetchall()
        return render_template('home.html',rows=rows,table_name=tb ,colnames=colnames)
    except Exception as e:
        raise e

@app.route('/delete',methods=['POST','GET'])
def delete():
    if request.method=='POST':
        db=getConnection()
        c=db.cursor()
        table_name=request.form['table_name']
        drop = ("DROP TABLE {tn}".format(tn=table_name))
        c.execute(drop)
    return redirect(url_for('index'))
@app.route('/drop',methods=['POST','GET'])
def drop():
    if request.method=='POST':
        table_name=request.form['table_name']
        db=getConnection()
        c=db.cursor()
        field_name=request.form['field_name']
        print(field_name)
        c.execute('DELETE FROM {tn} where Firstname = {fn}'.format(tn=table_name,fn=field_name))
        db.commit()
        db.close()
    return render_template('original.html')
    # return redirect(url_for('show'))
@app.route('/home')
def home():
    db=getConnection()
    c=db.cursor()
    cur=c.execute("select {col1},{col2},{col3},{col4},{col5},{col6},{col7} from {tn}".format(tn="EmployeeRegistration",col1="FIRSTNAME",col2="SURNAME",col3="NSSF_NUMBER",col4="STAFF_NUMBER",col5="BANK_NAME",col6="BANK_NUMBER",col7="POSITION_OR_TITLE"))
    row = cur.fetchall()
    rows=c.execute("select * from Dashboards where Viewer=='Hr'").fetchall()


    return render_template('home.html',nav_items=rows,row=row)

@app.route('/',methods=['POST','GET'])
def loginform():
    return render_template('login.html')

@app.route('/export_table')
def export_table():
        print(table_name)
        db=getConnection()
        c=db.cursor()
        c.execute('select * from {tn}'.format(tn=table_name))
        file_name=table_name +".csv"
        with open(file_name,'w') as out_csv_file:
            csv_out = csv.writer(out_csv_file)
            csv_out.writerow([d[0] for d in c.description])
            for row in c:
                csv_out.writerow(row)
        return redirect(url_for('index'))
        



@app.route('/login' ,methods=['POST','GET'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        role=request.form['role']
        db=getConnection()
        c=db.cursor()
        query=c.execute('SELECT * FROM Login WHERE Username = ? AND Password = ? AND Role  = ?', (username, password , role))
        rows = query.fetchall()
        if rows:
            if role=='Hr':
                return redirect(url_for('home'))
            elif role=='Admin':
                return redirect(url_for('index'))
            else:
                return render_template('login.html')
        else:
            print('Login failed!')
    return render_template('login.html')

ui.run()
