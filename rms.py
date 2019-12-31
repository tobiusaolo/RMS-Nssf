from flask import Flask, render_template, url_for, request,jsonify,redirect,g
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

#creating a connection to the database
DATABASE  = 'Database.db'
def getConnection():
    con = getattr(g,'_database',None)
    if con is None:
        con = g._database = sqlite3.connect(DATABASE)
    return con


@app.route('/',methods=['POST','GET'])
def index():
    return render_template('index.html')
##insert data into the database
@app.route('/Profile',methods=['POST','GET'])
def Profile():
    data = []
    if request.method=='POST':
        if request.files:
            image = request.files['image']
        Company_name = request.form['c_name']
        # Company_tin = request.form['c_tin']
        # Company_nssf_number = request.form['c_nssf_num']
        # Address=request.form['c_address']
        # Email = request.form['c_email']
        # Telephone = request.form['c_Tel']
        for v in request.form:
            data.append(request.form[v])
        #     data.append(image)
        # print(data)
        table_values = tuple(data[0:])
        db=getConnection()
        c=db.cursor()
        try:
            c.execute('''CREATE TABLE  IF NOT EXISTS  {tn} (Logo BLOB,Company_name VARCHAR(100) UNIQUE ,Company_tin VARCHAR(100) ,
            Company_nssf_number VARCHAR(100),Address VARCHAR(100)  ,Email  VARCHAR(100) ,Telephone  VARCHAR(100) )'''.format(tn=Company_name))
            c.execute('Insert INTO {tn} (Company_name,Company_tin,Company_nssf_number,Address,Email,Telephone) VALUES {tbv}'.format(tn=Company_name,tbv=table_values))
            db.commit()
            return redirect(url_for('index'))
        except Exception as e:
            raise e
    return render_template('index.html')
##adding department and list
@app.route('/department',methods=['POST','GET'])
def department():
    data=[]
    if request.method=='POST':
        for fm in request.form:
            data.append(request.form[fm])
        table_values = tuple(data[0:])
        db=getConnection()
        c=db.cursor()
        try:
            c.execute('''CREATE TABLE IF NOT EXISTS Departments(Department VARCHAR(100) UNIQUE,Number_of_members VARCHAR(100))''')
            c.execute('Insert INTO Departments(Department,Number_of_members) VALUES {tbv}'.format(tbv=table_values))
            db.commit()
            return redirect(url_for('department'))
        except Exception as e:
            raise e
    return render_template('department.html')
# ##Fetch employee data
# @app.route('/Fetch')
# def Fetch():
#     db = getConnection()
#     c = db.cursor()
#     query = c.execute('SELECT Emp_ID FROM Employee_Credentials')
#     emp_id = query.fetchall()
#     return render_template('employe_maintence.html',emp_id=emp_id)
###adding employee and removing employee
@app.route('/Employee')
def Employee():
    db = getConnection()
    c = db.cursor()
    query = c.execute('SELECT Emp_ID FROM Employee_Credentials')
    emp_id = query.fetchall()
    return render_template('employe_maintence.html',emp_id=emp_id)
##adding employee
@app.route('/Add',methods=['POST','GET'])
def Add():
    if request.method=='POST':
        emp_id =request.form['emp_id']
        tin_num=request.form['tin_num']
        nssf_num=request.form['nssf_num']
        designation=request.form['designation']
        status = request.form['status']
        join_date=request.form['join_date']
        db=getConnection()
        c=db.cursor()
        try:
            c.execute('''CREATE TABLE IF NOT EXISTS Employee_Credentials
            (Emp_ID VARCHAR(4000) UNIQUE,
            TIN_Number VARCHAR(400) UNIQUE ,NSSF_Number VARCHAR(1000) UNIQUE ,
            Designation VARCHAR(100), Employee_Status VARCHAR(100), Joining_Date DATE )''')
            c.execute('''Insert INTO Employee_Credentials(Emp_ID,TIN_Number,NSSF_Number,Designation,
            Employee_Status,Joining_Date) VALUES('{emp_id}','{tin_num}','{nssf_num}','{designation}','{status}','{join_date}')'''
                      .format(emp_id=emp_id,tin_num=tin_num,nssf_num=nssf_num,designation=designation,status=status,join_date=join_date))

            db.commit()
            return redirect(url_for('Fetch'))
        except Exception as e:
            raise e
    return render_template('employe_maintence.html',emp_id=emp_id)
##Add personal information to employees
@app.route('/Personal_Infor',methods=['POST','GET'])
def Personal_Infor():
    if request.method=='POST':
        ID = request.form['ID']
        first_name = request.form['first_name']
        last_name=request.form['last_name']
        date_of_birth=request.form['date_of_birth']
        marital_status=request.form['marital_status']
        gender=request.form['gender']
        nationality = request.form['nationality']
        db=getConnection()
        c=db.cursor()
        try:
            c.execute('''CREATE TABLE IF NOT EXISTS Personal_Infor(Emp_ID VARCHAR(4000) UNIQUE,
                        Firstname VARCHAR(400) ,Lastname VARCHAR(400) ,DOB DATE , Marital_Status VARCHAR(100), 
                        Gender VARCHAR(100) ,Nationality VARCHAR(400))''')
            c.execute('''INSERT INTO Personal_Infor(Emp_ID,Firtname,Lastname,DOB,Marital_Status,Gender,Nationality) 
            VALUES('{ID}','{first_name}','{last_name}','{date_of_birth}','{marital_status}','{gender}','nationality')'''.
                      format(ID=ID,first_name=first_name,last_name=last_name,date_of_birth=date_of_birth,marital_status=marital_status,gender=gender,nationality=nationality))
            db.commit()
            return  redirect(url_for('Fetch'))
        except Exception as e:
            raise e
    return render_template('employe_maintence.html')
##Add employee contact information
@app.route('/Contact_Infor',methods=['POST','GET'])
def Contact_Infor():
    if request.method=='POST':
        ID = request.form['ID']
        current_address=request.form['current_address']
        mobile=request.form['mobile']
        phone=request.form['phone']
        email=request.form['email']
        db=getConnection()
        c=db.cursor()
        try:
            c.execute('''CREATE TABLE IF NOT EXISTS Contact_Infor(Emp_ID VARCHAR(4000) UNIQUE,
                                    Current_Address VARCHAR(400) ,Mobile VARCHAR(400) ,Phone VARCHAR(100),Email VARCHAR(100))''')
            c.execute('''INSERT INTO Contact_Infor(Emp_ID,Current_Address,Mobile,Phone,Email) 
            VALUES('{ID}','{current_address}','{mobile}','{phone}','{email}')'''.
                      format(ID=ID,current_address=current_address,mobile=mobile,phone=phone,email=email))
            db.commit()
            return redirect(url_for('Fetch'))
        except Exception as e:
            raise e
    return render_template('employe_maintence.html')
###Bank Information
@app.route('/Bank_Infor',methods=['POST','GET'])
def Bank_Infor():
    if request.method=='POST':
        ID=request.form['ID']
        account_name=request.form['account_name']
        account_number= request.form['account_number']
        bank_name=request.form['bank_name']
        bank_branch=request.form['bank_branch']
        db=getConnection()
        c=db.cursor()
        try:
            c.execute('''CREATE TABLE IF NOT EXISTS Bank_Infor(Emp_ID VARCHAR(4000) UNIQUE,Account_Name VARCHAR(400),Account_Number VARCHAR(400),Bank_Name VARCHAR(400),Bank_Branch VARCHAR(400) )''')
            c.execute('''INSERT INTO Bank_Infor(Emp_ID,Account_Name,Account_Number,Bank_Name ,Bank_Branch) 
            VALUES('{ID}','{account_name}','{account_number}','{bank_name}','{bank_branch}')'''.format(ID=ID,account_name=account_name,account_number=account_number,bank_name=bank_name,bank_branch=bank_branch))
            db.commit()
            return redirect(url_for('Fetch'))
        except Exception as e:
            raise e
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
    db=getConnection()
    c=db.cursor()
    query = c.execute('SELECT * FROM Departments')
    rows = query.fetchall()
    return render_template('department_list.html',rows=rows)
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
@app.route('/update_settings')
def update_settings():
    try:
        db = getConnection()
        c = db.cursor()
        query = c.execute('SELECT * FROM Roles')
        rows = query.fetchall()
        redirect('settings')
    except Exception as e:
        raise e
    return render_template('settings.html', rows=rows)

@app.route('/settings')
def settings():
    db = getConnection()
    c = db.cursor()
    sql = c.execute('SELECT Firstname FROM Personal_Infor')
    depart = c.execute('SELECT Department FROM Departments')
    depart_row = depart.fetchall()
    sql_row = sql.fetchall()
    print(sql_row)
    return render_template('settings.html', sql_row=sql_row,depart_row=depart_row)
##Assigning employees roles
@app.route('/Role',methods=['POST','GET'])
def Role():
    db = getConnection()
    c = db.cursor()
    if request.method=='POST':
        name=request.form['name']
        role=request.form['role']
        password=request.form['password']
        department=request.form['department']
        try:
            c.execute('''CREATE TABLE IF NOT EXISTS Roles(Employee_name VARCHAR(100),Role VARCHAR(100),Password VARCHAR(100),Department VARCHAR(100))''')
            c.execute('''INSERT INTO Roles(Employee_name,Role,Password,Department) VALUES('{name}','{role}','{password}','{department}')'''.
                      format(name=name,role=role,password=password,department=department))
            db.commit()
            return redirect(url_for('update_settings'))
        except Exception as e:
            raise e
    return render_template('settings.html')
###change password
@app.route('/Change_Password')
def Change_Password():
    if request.method=='POST':
        name = request.form['name']
        c_password=request.form['cpassword']
        npassword = request.form['npassword']
    return render_template('settings.html')
if __name__ == "__main__":
   app.run(debug=True, host='0.0.0.0', port=5000)
