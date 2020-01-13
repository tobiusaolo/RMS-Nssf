import base64
import datetime
from datetime import datetime
import io
from io import BytesIO
import os

import numpy as np
from PIL import Image
from flask import Flask, render_template, url_for, request, jsonify, redirect, g
from flask import Flask, render_template, url_for, request,jsonify,redirect,g,send_file
from flaskwebgui import FlaskUI  # get the FlaskUI class
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from wtforms import TextField, SubmitField, TextAreaField , FieldList , FormField ,SelectField,Form,IntegerField,StringField
from wtforms.validators import  Length, Email, Required
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from sqlite3 import Error
from glob import glob
from fpdf import FPDF, HTMLMixin
import xlsxwriter

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///Database.db'
db  = SQLAlchemy(app)


class Data(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    company_name = db.Column(db.String(300))
    Tin_numer = db.Column(db.String(300))
    nssf_number = db.Column(db.String(300))
    address = db.Column(db.String(300))
    email = db.Column(db.String(300))
    telephone = db.Column(db.String(300))
    image=db.Column(db.LargeBinary)
db.create_all()
#creating a db to the database
DATABASE  = 'Database.db'


def getConnection():
    con = getattr(g,'_database',None)
    if con is None:
        con = g._database = sqlite3.connect(DATABASE)
    return con


@app.route("/Profile", methods=["GET", "POST"])
def Profile():
    if request.method=='POST':
        image = request.files['image']
        img = image.read()
        Company_name = request.form['c_name']
        tin = request.form['c_tin']
        c_nssf_num = request.form['c_nssf_num']
        c_address = request.form['c_address']
        c_email = request.form['c_email']
        c_Tel = request.form['c_Tel']
        ###insert data into the table in the sqlite database
        new_file=Data(company_name=Company_name,Tin_numer=tin,
                       nssf_number=c_nssf_num,address=c_address,
                       email=c_email,telephone=c_Tel,image=img)
        db.session.add(new_file)
        db.session.commit()
    return render_template('index.html')

@app.route('/',methods=['POST','GET'])
def index():
    try:
        file = Data.query.filter_by(id=1).first()
        img = base64.b64encode(file.image).decode('ascii')
    except:
        img="User"
    return render_template('index.html',img=img)

##Edit company profile
@app.route('/Edit_Profile',methods=['POST','GET'])
def Edit_Profile():
    data= Data.query.filter_by(id=1).first()
    cname = data.company_name
    tin=data.Tin_numer
    nssf=data.nssf_number
    address=data.address
    email=data.email
    tel=data.telephone
    file = Data.query.filter_by(id=1).first()
    img = base64.b64encode(file.image).decode('ascii')
    return  render_template('edit.html',cname=cname,tin=tin,nssf=nssf,address=address,email=email,tel=tel,img=img)
@app.route('/Update_Profile',methods=['POST','GET'])
def Update_Profile():
    if request.method=='POST':
        image=request.files['image']
        img = image.read()
        company_name=request.form['company_name']
        nssf=request.form['nssf']
        tin=request.form['tin']
        address=request.form['address']
        email=request.form['email']
        tel = request.form['tel']
        try:
            df = db.session.query(Data).filter_by(id=1).one()
            if df != []:
                df.company_name = company_name
                df.Tin_numer = tin
                df.nssf_number = nssf
                df.address = address
                df.email = email
                df.telephone = tel
                db.session.add(df)
                db.session.commit()
                return redirect(url_for('Edit_Profile'))
        except Exception as  e:
            raise e
    return render_template('edit.html')
##adding department and list
@app.route('/department',methods=['POST','GET'])
def department():
    if request.method=='POST':
        departments=request.form['departments']
        db=getConnection()
        c=db.cursor()
        try:
            c.execute("Insert INTO Departments(Department) VALUES('{tbv}')".format(tbv=departments))
            db.commit()
            db.close()
            return redirect(url_for('Department_list'))
        except Exception as e:
            raise e
    return render_template('department.html')
@app.route('/Employee',methods=['POST','GET'])
def Employee():
    data = []
    if request.method == 'POST':
        for form in request.form:
            data.append(request.form[form])
        table_data = tuple(data)
        db = getConnection()
        c = db.cursor()
        t=db.cursor()
        try:
            c.execute('''CREATE TABLE IF NOT EXISTS Employee_Data(Emp_ID VARCHAR(100),TIN_NUMBER VARCHAR(100),
            NSSF_NUMBER VARCHAR(100),DESIGNATION VARCHAR(100),STATUS VARCHAR(100) ,JOIN_DATE DATE,FIRSTNAME VARCHAR(100),
            LASTNAME VARCHAR(100),DOB DATE ,MARITAL_STATUS VARCHAR(100),GENDER VARCHAR(100),NATIONALITY VARCHAR(100),
            CURRENT_ADDRESS VARCHAR(100),MOBILE VARCHAR(10),PHONE VARCHAR(10),EMAIL VARCHAR(100),ACCOUNT_NAME VARCHAR(100),
            ACCOUNT_NUMBER VARCHAR(100) ,BANK_NAME VARCHAR(100),BANK_BRANCH VARCHAR(100),ATTENDANCE_STATUS VARCHAR(100))''')

            t.execute('''INSERT INTO Employee_Data(Emp_ID,TIN_NUMBER,NSSF_NUMBER,DESIGNATION,STATUS,JOIN_DATE,FIRSTNAME,
            LASTNAME,DOB,MARITAL_STATUS,GENDER,NATIONALITY,CURRENT_ADDRESS,MOBILE,PHONE,EMAIL,ACCOUNT_NAME,ACCOUNT_NUMBER,BANK_NAME
            ,BANK_BRANCH,ATTENDANCE_STATUS)  VALUES {table_values}'''.format(table_values=table_data))
            db.commit()
            db.close()
            return redirect(url_for('Employee'))
        except Exception as e:
            raise e
    return render_template('employe_maintence.html')
####leave and attendance
@app.route('/Leave')
def Leave():
    db = getConnection()
    c = db.cursor()
    query= c.execute('SELECT FIRSTNAME FROM Employee_Data')
    sql_rows =query.fetchall()
    return render_template('leave.html',sql_rows=sql_rows)
###Public holidays
@app.route('/Holidays',methods=['POST','GET'])
def Holidays():
    data = []
    if request.method=='POST':
        for fm in request.form:
            data.append(request.form[fm])
        form_values =tuple(data[0:])
        db=getConnection()
        c=db.cursor()
        try:
            c.execute('''CREATE TABLE IF NOT EXISTS Holidays(Public_Holiday VARCHAR(4000) ,Public_Date DATE ,Personal_Event VARCHAR(100),Personal_Date DATE ,
            Company_Event VARCHAR(100),Company_Event_Date DATE )''')
            c.execute('Insert INTO Holidays(Public_Holiday,Public_Date,Personal_Event,Personal_Date,Company_Event,Company_Event_Date) VALUES {tbv}'.format(tbv=form_values))
            db.commit()
            db.close()
        except Exception as e:
            raise e
    return render_template('leave.html')
###sick leave
@app.route('/Sick_Leave',methods=['POST','GET'])
def Sick_Leave():
    if request.method=='POST':
        name=request.form['name']
        start_date=request.form['start_date']
        end_date=request.form['end_date']
        replacement=request.form['replacement']
        db=getConnection()
        c=db.cursor()
        try:
            c.execute('''CREATE TABLE IF NOT EXISTS Sick_Leave(Employee_Name VARCHAR(100),Replacement VARCHAR(100),Start_Date DATE ,End_Date DATE)''')
            c.execute("Insert INTO Sick_Leave(Employee_Name,Replacement,Start_Date,End_Date) VALUES('{name}','{rep}','{start_date}','{end_date}')".format(name=name,rep=replacement,start_date=start_date,end_date=end_date))
            db.commit()
            db.close()
            return  redirect(url_for('Leave'))
        except Exception as e:
            raise e
    return render_template('leave.html')
###Asign a vacation
@app.route('/Vacation',methods=['POST','GET'])
def Vacation():
    if request.method=='POST':
        name=request.form['name']
        start_date=request.form['start_date']
        end_date=request.form['end_date']
        replacement = request.form['replacement']
        db = getConnection()
        c = db.cursor()
        try:
            c.execute('''CREATE TABLE IF NOT EXISTS Vacation(Employee_Name VARCHAR(4000),Replacement VARCHAR(100),Start_Date DATE ,End_Date DATE)''')
            c.execute("Insert INTO Vacation(Employee_Name,Replacement,Start_Date,End_Date) VALUES('{name}','{rep}','{start_date}','{end_date}')".format(name=name,rep=replacement,start_date=start_date, end_date=end_date))
            db.commit()
            db.close()
            return  redirect(url_for('Leave'))
        except Exception as e:
            raise e
    return render_template('leave.html')
###set working days
@app.route('/working_days',methods=['POST','GET'])
def working_days():
    if request.method=='POST':
        data = request.form.getlist("day")
        db=getConnection()
        c=db.cursor()
        try:
            c.execute("""CREATE TABLE IF NOT EXISTS Working_days(Work_Day VARCHAR(100))""")
            for d in data:
                c.execute("""INSERT INTO Working_days(Work_Day) VALUES('{tbv}')""".format(tbv=d))
            db.commit()
            db.close()
        except Exception as e:
            raise e
    return  render_template('working_days.html')
##employee list
@app.route('/Employee_list',methods=['POST','GET'])
def Employee_list():
    # df = []
    db = getConnection()
    c = db.cursor()
    query = c.execute('''SELECT TIN_NUMBER,NSSF_NUMBER,STATUS,JOIN_DATE,FIRSTNAME,
            LASTNAME,EMAIL,ATTENDANCE_STATUS FROM Employee_Data''')
    rows = query.fetchall()
    # t = db.cursor()
    # sql = t.execute('''SELECT Employee_name,Role,Department FROM Roles''')
    # sql_row = sql.fetchall()
    # for i, x in zip(sql_row,rows):
    #     data = i + x
    #     df.append(data)
    return render_template('employee_list.html',df=rows)
##activate status
@app.route('/activate',methods=['POST','GET'])
def activate():
    if request.method=='POST':
        name = request.form['name']
        db = getConnection()
        d= db.cursor()
        try:
            d.execute('''UPDATE Employee_Data SET ATTENDANCE_STATUS=('Active') WHERE FIRSTNAME=('{nm}')'''.format(nm=name))
            db.commit()
            db.close()
            return  redirect(url_for('Employee_list'))
        except Exception as e:
            raise e
    return  render_template('employee_list.html')
##Fire employee
@app.route('/Fire_Employee',methods=['POST','GET'])
def Fire_Employee():
    if request.method=='POST':
        name = request.form['name']
        db = getConnection()
        d= db.cursor()
        try:
            d.execute('''UPDATE Employee_Data SET ATTENDANCE_STATUS=('Inactive') WHERE FIRSTNAME=('{nm}')'''.format(nm=name))
            db.commit()
            db.close()
            return  redirect(url_for('Employee_list'))
        except Exception as e:
            raise e
    return render_template('employee_list.html.html')
##department list
@app.route('/Department_list',methods=['POST','GET'])
def Department_list():
    db=getConnection()
    c=db.cursor()
    try:
        query = c.execute('SELECT * FROM Departments')
        # sql=c.execute('SELECT Department FROM Role')
        # sql_rows=sql.fetchall().count()
        rows = query.fetchall()
        db.close()
    except:
        c.execute('''CREATE TABLE IF NOT EXISTS Departments(Department VARCHAR(100) UNIQUE,Number_of_members VARCHAR(100))''')
        db.commit()
        db.close()
    return render_template('department.html',rows=rows)


###Delete department
@app.route('/Delete_Department',methods=['POST','GET'])
def Delete_Department():
    if request.method=='POST':
        depart=request.form['depart']
        db=getConnection()
        c=db.cursor()
        try:
            c.execute('''DELETE FROM Departments WHERE Department=('{nm}') '''.format(nm=depart))
            db.commit()
            db.close()
            return redirect(url_for('Department_list'))
        except Exception as e:
            raise e
    return  render_template('department_list.html')
##attendance
@app.route('/Attendance',methods=['POST','GET'])
def Attendance():
    df = []
    db=getConnection()
    c=db.cursor()
    query = c.execute('''SELECT FIRSTNAME FROM Employee_Data''')
    rows = query.fetchall()
    t=db.cursor()
    sql = t.execute('''SELECT Role FROM Roles''')
    sql_row = sql.fetchall()
    for i,x in zip(rows,sql_row):
        data = i+x
        df.append(data)
    r = len(rows)
    return render_template('attendance.html',rows=rows,r=r)
###take attendance
@app.route('/Take_Attendance',methods=['POST','GET'])
def Take_Attendance():
    data=[]
    if request.method=='POST':
        today=datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        for v in request.form:
            data.append(request.form[v])
        data.append(today)
        table_insert = tuple(data)
        db = getConnection()
        c=db.cursor()
        try:
            c.execute("""CREATE TABLE IF NOT EXISTS Attendance(FIRSTNAME VARCHAR(100) ,Attendance VARCHAR(100),Day_Date DATE)""")
            c.execute("""INSERT INTO Attendance(FIRSTNAME,Attendance,Day_Date) VALUES {tbv}""".format(tbv=table_insert))
            db.commit()
            db.close()
            return  redirect(url_for('Attendance'))
        except Exception as e:
            raise  e
    return render_template('attendance.html')
#####salary
@app.route('/salary')
def salary():
    db = getConnection()
    c = db.cursor()
    try:
        emp_data=c.execute('SELECT * FROM Employee_Data')
        emp_rows=emp_data.fetchall()
        query = c.execute('SELECT * FROM Finances')
        sql_rows = query.fetchall()
    except Exception as e:
        c = db.cursor()
        c.execute('''CREATE TABLE  Finances(Employee_Name VARCHAR(100),Residence_type VARCHAR(50),Employee_type VARCHAR(100),Gross_pay VARCHAR(100),Nssf_contrb VARCHAR(100),Paye VARCHAR(100),Total_Dect VARCHAR(100),Net_pay VARCHAR(100))''')
        db.commit()
        return redirect(url_for('salary'))


    db.close()   
    return render_template('salary.html',data1=sql_rows,emp_rows=emp_rows)
@app.route('/add_detail',methods=['POST','GET'])
def add_detail():
    detail=[]
    if request.method == 'POST':
        Employee_name=request.form['name']
        detail.append(Employee_name)
        residence_type=request.form['residence_nature']
        detail.append(residence_type)
        employee_type=request.form['emp_type']
        detail.append(employee_type)
        
        basic_salary=request.form['bsalary']
        detail.append(float(basic_salary))
        #calculate NSSf contribution
        #5% calculation
        employee_contrnssf=0.05*float(basic_salary)
        #employer NSSf contribution
        employeer_contrnssf=0.1*float(basic_salary)
        nssf_contribution = employee_contrnssf+employeer_contrnssf
        detail.append(nssf_contribution)

        #calculate payee
       
        if residence_type=='Resident':
             #Paye for residents
            if float(basic_salary)<235000:
                paye=0
                
            elif float(basic_salary) in range(235000,335000):
                paye=0.1*float(basic_salary)
                
            elif float(basic_salary) in range(335000,410000):
                paye=10000 + 0.2*float(basic_salary)
                
            elif float(basic_salary)>410000:
                paye=25000+0.3*float(basic_salary)
                
            elif float(basic_salary)>10000000:
                paye=25000+0.3*float(basic_salary)+0.1*float(basic_salary)
                
            else:
                print("Enter valid money for the employeee")

        elif residence_type == 'Non-Resident':
            #paye for non residents
            if float(basic_salary)<335000:
                paye=0.1*float(basic_salary)
                
            elif float(basic_salary) in range(335000,410000):
                paye=33500 + 0.2*float(basic_salary)
                
            elif float(basic_salary)>410000:
                paye=48500+0.3*float(basic_salary)
                
            elif float(basic_salary)>10000000:
                paye=48500+0.3*float(basic_salary)+0.1*float(basic_salary)
                
            else:
                print("Enter valid money for the employeee")


        else:
            print("warning this field is required !!!")
        detail.append(paye)
        tt_deductions=paye+nssf_contribution
        detail.append(tt_deductions)
        Net_salary=float(basic_salary)-tt_deductions
        detail.append(Net_salary)
        
        arr=[str(i) for i in detail]
        detail_data = tuple(arr)
  
        db = getConnection()
        c = db.cursor()
        try:
            c.execute('''CREATE TABLE IF NOT EXISTS Finances(Employee_Name VARCHAR(100),Residence_type VARCHAR(50),Employee_type VARCHAR(100),Gross_pay VARCHAR(100),Nssf_contrb VARCHAR(100),Paye VARCHAR(100),Total_Dect VARCHAR(100),Net_pay VARCHAR(100))''')
            c.execute('''Insert INTO Finances(Employee_Name,Residence_type,Employee_type,Gross_pay,Nssf_contrb,Paye,Total_Dect,Net_pay) VALUES {table_value}'''.format(table_value=detail_data))
            db.commit()
            db.close()
            return  redirect(url_for('salary'))
        except Exception as e:
            raise e   
    return render_template('salary.html')
##employee salaries
@app.route('/Salaries')
def Salaries():

    db = getConnection()
    c = db.cursor()
    gallowances = c.execute('SELECT * FROM Allowances')
    rallowances =  gallowances.fetchall()
    gpayment = c.execute('SELECT * FROM Payment')
    rpay_list = gpayment.fetchall()


    return render_template('Salaries.html',rallowances=rallowances,rpay_list=rpay_list)
# ##user settings
# @app.route('/update_settings')
# def update_settings():
#    if request.method=='POST':
#        try:
#            db = getConnection()
#            c = db.cursor()
#            query = c.execute('SELECT * FROM Roles')
#            rows = query.fetchall()
#            return redirect('settings')
#     return render_template('settings.html', rows=rows)
#Allowances
@app.route('/gen_slip',methods=['POST','GET'])
def gen_slip():
    if request.method=='POST':
        db = getConnection()
        c = db.cursor()
        new_data=request.form['myFile']
        company_details=c.execute('SELECT * FROM  Artistry')
        crows = company_details.fetchall()
        gallowances = c.execute('''SELECT * FROM Allowances WHERE Emp_Name=('{nd}')'''.format(nd=new_data))
        rallowances =  gallowances.fetchall()
        gpayment = c.execute('''SELECT * FROM Payment WHERE Emp_Name=('{name}')'''.format(name=new_data))
        rpay_list = gpayment.fetchall()
        gf = c.execute('''SELECT * FROM Finances WHERE Employee_Name=('{name}')'''.format(name=new_data))
        rf_list = gf.fetchall()

        pdf = FPDF(format='letter')
        pdf.add_page()
        page_width = pdf.w - 2 * pdf.l_margin
        col_width = page_width/4
        th =12
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(200, 5, crows[0][1])
        pdf.ln()
        pdf.multi_cell(200, 5, crows[0][4])
        pdf.ln()
        pdf.multi_cell(200, 5, 'Monthly Payslip')
        pdf.ln()
        pdf.multi_cell(0, 5, ('Employee Name: %s' % rpay_list[0][0]))
        pdf.ln()
        pdf.multi_cell(0, 5, ('Designation: %s' % rf_list[0][1]))
        pdf.ln()
        pdf.multi_cell(0, 5, ('Designation: %s' % rpay_list[0][4]))
        pdf.ln()
        pdf.multi_cell(200, 5, 'Allowances')
        pdf.ln()
        for row in rallowances:
            pdf.cell(col_width, th, str(row[1]), border=1)
            pdf.cell(col_width, th, row[2], border=1)
            pdf.cell(col_width, th, row[3], border=1)
            pdf.ln(10)
        pdf.ln(5)
        pdf.multi_cell(200, 5, 'Deductions And Net Pay')
        pdf.ln(5)
        for drow in rf_list :
           pdf.cell(col_width, th, "Nssf Contribution", border=1)
           pdf.cell(col_width, th, drow[4], border=1)
           pdf.ln(10)
           pdf.cell(col_width, th, "PAYE", border=1)
           pdf.cell(col_width, th, drow[5], border=1)
           pdf.ln(10)
           pdf.cell(col_width, th, "Total Deduction", border=1)
           pdf.cell(col_width, th, drow[6], border=1)
           pdf.ln(10)
           pdf.cell(col_width, th, "Gross Pay", border=1)
           pdf.cell(col_width, th, drow[2], border=1)
           pdf.ln(10)
           pdf.cell(col_width, th, "Net Pay", border=1)
           pdf.cell(col_width, th, drow[7], border=1)

        pdf.output("home.pdf")

    return send_file('home.pdf',as_attachment=True)
@app.route('/allowances')
def allowances():
    db = getConnection()
    c = db.cursor()
    try:
        #select employe name from employee table
        semploy=c.execute('SELECT * FROM Employee_Data')
        serows=semploy.fetchall()
        #select allowance type from allowance type table
        atype = c.execute('SELECT * FROM Allowance_types')
        arows = atype.fetchall()
        #select allownaces
        query = c.execute('SELECT * FROM Allowances')
        allowance_rows = query.fetchall()
    except Exception as e:
        c = db.cursor()
        #creat allowances table is not existing
        c.execute('''CREATE TABLE IF NOT EXISTS Allowances(Emp_Name VARCHAR(100),Allowance_type VARCHAR(100),Issue_Date DATE,Amount VARCHAR(100))''')
        #create employee table is not exist
        #create allowance type  table is not exist
        c.execute('''CREATE TABLE IF NOT EXISTS Allowance_types(Allowance_id VARCHAR(100),Allowance_type VARCHAR(100),Creation_Date DATE)''')
        db.commit()
        return redirect(url_for('allowances'))


    db.close()   
    return render_template('allowances.html',data1=allowance_rows,arows=arows,serows=serows)
@app.route('/add_allowance',methods=['POST','GET'])
def add_allowance():
    dallowance=[]
    if request.method=='POST':
        d_id=request.form['a_id']
        dallowance.append(d_id)
        atype=request.form['a_type']
        dallowance.append(atype)
        cdate=request.form['a_date']
        dallowance.append(cdate)
        arr4=[str(i) for i in dallowance]
        dallowance_data = tuple(arr4)
        db = getConnection()
        c = db.cursor()
        try:
            c.execute('''INSERT INTO Allowance_types(Allowance_id,Allowance_type,Creation_Date)  VALUES {table_value}'''.format(table_value=dallowance_data))
            db.commit()
            db.close()
        except Exception as e:
            raise e
    
    return  redirect(url_for('allowances'))

@app.route('/issue_allowance',methods=('POST','GET'))
def issue_allowance():
    allowance = []
    if request.method == 'POST':
        emp_name=request.form['a_empname']
        allowance.append(emp_name)
        allowance_type=request.form['a_type']
        allowance.append(allowance_type)
        Issue_date=request.form['a_date']
        allowance.append(Issue_date)
        amt=request.form['a_ammount']
        allowance.append(amt)
        arr2=[str(i) for i in allowance]
        allowance_data = tuple(arr2)
        db = getConnection()
        c = db.cursor()
        try:
            c.execute('''INSERT INTO Allowances(Emp_Name,Allowance_type,Issue_Date,Amount)  VALUES {table_values}'''.format(table_values=allowance_data))
            db.commit()
            db.close()
            return redirect(url_for('allowances'))
        except Exception as e:
            raise e

    return render_template('allowances.html')

@app.route('/deductions')
def deductions():
    db = getConnection()
    c = db.cursor()
    try:
        #select employe name from employee table
        semploy=c.execute('SELECT * FROM Employee_Data')
        serows=semploy.fetchall()
        #select allowance type from allowance type table
        dtype = c.execute('SELECT * FROM Deduction_types')
        drows = dtype.fetchall()
        #select allownaces
        query = c.execute('SELECT * FROM  Deduction')
        adeduction_rows = query.fetchall()
    except Exception as e:
        c = db.cursor()
        #creat allowances table is not existing
        c.execute('''CREATE TABLE IF NOT EXISTS Deduction(Emp_Name VARCHAR(100),deduction_type VARCHAR(100),Issue_Date DATE,Amount VARCHAR(100))''')
        #create employee table is not exist
        #create allowance type  table is not exist
        c.execute('''CREATE TABLE IF NOT EXISTS Deduction_types(Dect_id VARCHAR(100),Deduction_type VARCHAR(100),Description VARCHAR(100),Creation_Date DATE)''')
        db.commit()
        return redirect(url_for('deductions'))


    db.close()
    return render_template('deductions.html',adeduction_rows=adeduction_rows,drows=drows,serows=serows)
@app.route('/add_deduction',methods=['POST','GET'])
def add_deduction():
    dd=[]
    if request.method=='POST':
        d_id=request.form['a_id']
        dd.append(d_id)
        dtype=request.form['d_type']
        dd.append(dtype)
        descrip=request.form['descip']
        dd.append(descrip)
        cdate=request.form['a_date']
        dd.append(cdate)
        arr4=[str(i) for i in dd]
        dd_data = tuple(arr4)
        db = getConnection()
        c = db.cursor()
        try:
            c.execute('''INSERT INTO Deduction_types(Dect_id,Deduction_type,Description,Creation_Date)  VALUES {table_value}'''.format(table_value=dd_data))
            db.commit()
            db.close()
        except Exception as e:
            raise e
    
    return  redirect(url_for('deductions'))
@app.route('/compute_deduction',methods=['POST','GET'])
def compute_deduction():
    edd = []
    if request.method == 'POST':
        emp_name=request.form['a_empname']
        edd.append(emp_name)
        allowance_type=request.form['d_type']
        edd.append(allowance_type)
        Issue_date=request.form['a_date']
        edd.append(Issue_date)
        amt=request.form['a_ammount']
        edd.append(amt)
        arr2=[str(i) for i in edd]
        edd_data = tuple(arr2)
        db = getConnection()
        c = db.cursor()
        try:
            c.execute('''INSERT INTO Deduction(Emp_Name,deduction_type,Issue_Date,Amount)  VALUES {table_values}'''.format(table_values=edd_data))
            db.commit()
            db.close()
            return redirect(url_for('deductions'))
        except Exception as e:
            raise e

    return render_template('deductions.html')
#NSSF submission
@app.route('/nssf')
def nssf():
    return render_template('nssf_subf.html')
@app.route('/nssf_sub',methods=['POST','GET'])
def nssf_sub():
    if request.method=='POST':
        syear=request.form['year']
        submonth=request.form['sMonth']
        
        db = getConnection()
        c = db.cursor()
        company_details=c.execute('SELECT * FROM  Artistry')
        crows = company_details.fetchall()

        
        ford=c.execute("select Employee_Data.Emp_ID,Employee_Data.Emp_ID,Employee_Data.NSSF_NUMBER,Finances.Residence_type,Employee_Data.FIRSTNAME,Finances.Gross_pay,Finances.Nssf_contrb,Finances.Paye,Finances.Total_Dect,Employee_Data.MOBILE from Payment JOIN Finances ON(Payment.Emp_Name=Finances.Employee_Name) JOIN Employee_Data ON(Payment.Emp_Name= Employee_Data.FIRSTNAME) WHERE Payment.Paid_month=('{nmonth}')".format(nmonth=submonth))
        drows = ford.fetchall()
        #sum
        tsum=c.execute("select SUM(Finances.Total_Dect)from Payment JOIN Finances ON(Payment.Emp_Name=Finances.Employee_Name) JOIN Employee_Data ON(Payment.Emp_Name= Employee_Data.FIRSTNAME) WHERE Payment.Paid_month=('{nmonth}')".format(nmonth=submonth))
        tsumval = tsum.fetchall()

        workbook = xlsxwriter.Workbook('nssf.xlsx')
       #writing excel headers
        worksheet = workbook.add_worksheet()
        cell_format = workbook.add_format()
     #create a format to use in the merged range
        cell_format.set_font_color('Sliver')
        coname=crows[0][1]
        nssf=crows[0][3]
        ttr=1233333
        # print(tsumval[0][0])
    
        nmembers=len(drows)
        year=syear
        nMonth=submonth
        merge_format=workbook.add_format({'bold':1,'border':1,'align':'center','valign':'vcenter'})
        # merge_format2=workbook.add_format({'fg_color':'sliver'})
        #merge 7 cells
        worksheet.merge_range('A1:H1','NATIONAL SOCIAL SECURITY FUND',merge_format)
        worksheet.merge_range('A2:H2','MONTHLY SCHEDULE',merge_format)
        worksheet.merge_range('A3:H3','C-SPEED MOBILE',merge_format)
        worksheet.write('C6','Company Name')
        worksheet.write('C7','Company NSSF Number')
        worksheet.write('C8','Total Amount')
        worksheet.write('C9','No.of members')
        worksheet.write('D6',coname)
        worksheet.write('D7',nssf)
        worksheet.write('D8',ttr)
        worksheet.write('D9',nmembers)
        worksheet.write('E6','Year')
        worksheet.write('E7','Month')
        worksheet.write('F6',year)
        worksheet.write('F7',nMonth)
        #legend
        worksheet.write('G4','Legend')
        worksheet.merge_range('G5:H5','Calculated Protected')
        worksheet.merge_range('G6:H6','Required')
        worksheet.merge_range('G7:H7','Optional')
        #contribution
        worksheet.write('I3','NORMAL')
        worksheet.write('I4','BONUS')
        worksheet.write('I5','ARREAR')
        worksheet.write('I6','MULTIPLE')
        worksheet.write('I7','10%CONTRIBUTION')
        worksheet.write('I8','5%CONTRIBUTION')
        worksheet.write('I9','SPECIAL CONTRIBUTION')
        worksheet.write('I10','INTEREST')
        #Description
        worksheet.write('J2','DESCRIPTION')
        worksheet.write('J3','15% normal contribution')
        worksheet.write('J4','15% bonus contribution')
        worksheet.write('J5','15% arrear contribution')
        worksheet.write('J6','15% contributions paid more than once')
        worksheet.write('J7','10% contribution')
        worksheet.write('J8','5% contribution')
        worksheet.write('J9','Special contribution')
        worksheet.write('J10','Interest contribution')
        #column headers
        worksheet.write('A12','NO')
        worksheet.write('B12','NationalID/StaffNo')
        worksheet.write('C12','Employee NSSF Number')
        worksheet.write('D12','Contribution Type')
        worksheet.write('E12','Employee Names')
        worksheet.write('F12','Employee Gross Pay')
        worksheet.write('G12','Employee Contribution')
        worksheet.write('H12','Employer Contribution')
        worksheet.write('I12','Total Contribution')
        worksheet.write('J12','Telephone Number')
        #add values to the file
        
        for i, row in enumerate(drows):
            for j, value in enumerate(row):
                worksheet.write(i+12, j, row[j])
        workbook.close() 
  
    
    return redirect(url_for('nssf'))

@app.route('/pay')
def pay():
    
    try:
        db = getConnection()
        c = db.cursor()
        # #name,department,date,amount,period
        # # query = c.execute('SELECT * FROM Employee_Data')
        # # emp_rows = query.fetchall()
        depart = c.execute('SELECT * FROM Finances')
        depart_row = depart.fetchall()
        pay_list = c.execute('SELECT * FROM Payment')
        dpay_list = pay_list.fetchall()
        
    except Exception as e:
        c = db.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS Payment(Emp_Name VARCHAR(100),Salary VARCHAR(15),Paid_month VARCHAR(15),pYear VARCHAR(10),Issue_Date DATE)''')
        db.commit()
        return redirect(url_for('pay'))
        
    
    return render_template('pay.html',pay_list=dpay_list,Finance=depart_row)
    
@app.route('/add_tpaylist',methods=['POST','GET'])
def add_tpaylist():
    list_data = []
    db = getConnection()
    c = db.cursor()
    if request.method=='POST':
        name=request.form['emp_id']
        list_data.append(name)
        salary=request.form['bsalary']
        list_data.append(salary)
        vmonth=request.form['vMonth']
        list_data.append(vmonth)
        vyear=request.form['vyear']
        list_data.append(vyear) 
        vdate=request.form['vdate']
        list_data.append(vdate)
        arr3=[str(i) for i in list_data]
        main_add = tuple(arr3)
        try:
            c.execute('''CREATE TABLE IF NOT EXISTS Payment(Emp_Name VARCHAR(100),Salary VARCHAR(15),Paid_month VARCHAR(15),pYear VARCHAR(10),Issue_Date DATE)''')
           
            c.execute('''INSERT INTO Payment(Emp_Name,Salary,Paid_month,pYear,Issue_Date)  VALUES {table_value}'''.format(table_value=main_add))
            db.commit()
            db.close()
            return redirect(url_for('pay'))
        except Exception as e:
            raise e

    return render_template('pay.html',finance=Finance_row)


@app.route('/settings')
def settings():
    db = getConnection()
    c = db.cursor()
    query = c.execute('SELECT FIRSTNAME FROM Employee_Data')
    sql_rows = query.fetchall()
    depart = c.execute('SELECT Department FROM Departments')
    depart_row = depart.fetchall()
    query = c.execute('SELECT * FROM Roles')
    rows = query.fetchall()
    
    return render_template('settings.html', sql_rows=sql_rows,depart_row=depart_row, rows=rows)
##Delete user
@app.route('/Delete_User',methods=['POST','GET'])
def Delete_User():
    if request.method=='POST':
        name = request.form['name']
        db=getConnection()
        c=db.cursor()
        try:
            c.execute('''DELETE FROM Roles WHERE Employee_name=('{nm}') '''.format(nm=name))
            db.commit()
            db.close()
            return  redirect(url_for('settings'))
        except Exception as e:
            raise  e
    return  render_template('settings.html')
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
            db.close()
            return redirect(url_for('settings'))
        except Exception as e:
            raise e
    return render_template('settings.html')
###change password
@app.route('/Change_Password',methods=['POST','GET'])
def Change_Password():
    if request.method=='POST':
        name = request.form['name']
        npassword = request.form['npassword']
        db=getConnection()
        c=db.cursor()
        try:
            c.execute('''UPDATE Roles SET Password =('{ps}') WHERE Employee_name=('{nm}')'''.format(ps=npassword, nm=name))
            db.commit()
            db.close()
            return redirect(url_for('settings'))
        except Exception as e:
            raise e
    return render_template('settings.html')
if __name__ == "__main__":

#    app.run( )

#    app.run(debug=True)
   app.run( )

