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
from fpdf import FPDF, HTMLMixin

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
            db.close()
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
            db.close()
            return redirect(url_for('department'))
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
        try:
            c.execute('''CREATE TABLE IF NOT EXISTS Employee_Data(Emp_ID VARCHAR(100),TIN_NUMBER VARCHAR(100),
            NSSF_NUMBER VARCHAR(100),DESIGNATION VARCHAR(100),STATUS VARCHAR(100) ,JOIN_DATE DATE,FIRSTNAME VARCHAR(100),
            LASTNAME VARCHAR(100),DOB DATE ,MARITAL_STATUS VARCHAR(100),GENDER VARCHAR(100),NATIONALITY VARCHAR(100),
            CURRENT_ADDRESS VARCHAR(100),MOBILE VARCHAR(10),PHONE VARCHAR(10),EMAIL VARCHAR(100),ACCOUNT_NAME VARCHAR(100),
            ACCOUNT_NUMBER VARCHAR(100) ,BANK_NAME VARCHAR(100),BANK_BRANCH VARCHAR(100),ATTENDANCE_STATUS VARCHAR(100))''')

            c.execute('''INSERT INTO Employee_Data(Emp_ID,TIN_NUMBER,NSSF_NUMBER,DESIGNATION,STATUS,JOIN_DATE,FIRSTNAME,
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
        db=getConnection()
        c=db.cursor()
        try:
            c.execute('''CREATE TABLE IF NOT EXISTS Sick_Leave(Employee_Name VARCHAR(4000) ,Start_Date DATE ,End_Date DATE)''')
            c.execute("Insert INTO Sick_Leave(Employee_Name,Start_Date,End_Date) VALUES('{name}','{start_date}','{end_date}')".format(name=name,start_date=start_date,end_date=end_date))
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
        db = getConnection()
        c = db.cursor()
        try:
            c.execute('''CREATE TABLE IF NOT EXISTS Vacation(Employee_Name VARCHAR(4000),Start_Date DATE ,End_Date DATE)''')
            c.execute("Insert INTO Vacation(Employee_Name,Start_Date,End_Date) VALUES('{name}','{start_date}','{end_date}')".format(name=name, start_date=start_date, end_date=end_date))
            db.commit()
            db.close()
            return  redirect(url_for('Leave'))
        except Exception as e:
            raise e
    return render_template('leave.html')
###set working days
@app.route('/working_days')
def working_days():
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
@app.route('/Department_list')
def Department_list():
    db=getConnection()
    c=db.cursor()
    query = c.execute('SELECT * FROM Departments')
    rows = query.fetchall()
    db.close()
    return render_template('department_list.html',rows=rows)
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
    query = c.execute('''SELECT JOIN_DATE,Emp_ID,FIRSTNAME FROM Employee_Data''')
    rows = query.fetchall()
    t=db.cursor()
    sql = t.execute('''SELECT Role FROM Roles''')
    sql_row = sql.fetchall()
    for i,x in zip(rows,sql_row):
        data = i+x
        df.append(data)
    return render_template('attendance.html',rows=df)
#####salary
@app.route('/salary')
def salary():
    db = getConnection()
    c = db.cursor()
    try:
        query = c.execute('SELECT * FROM Finances')
        sql_rows = query.fetchall()
    except Exception as e:
        c = db.cursor()
        c.execute('''CREATE TABLE  Finances(Employee_Name VARCHAR(100),Residence_type VARCHAR(50),Employee_type VARCHAR(100),Gross_pay VARCHAR(100),Nssf_contrb VARCHAR(100),Paye VARCHAR(100),Total_Dect VARCHAR(100),Net_pay VARCHAR(100))''')
        db.commit()
        return redirect(url_for('salary'))


    db.close()   
    return render_template('salary.html',data1=sql_rows)
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
    return render_template('Salaries.html')
<<<<<<< HEAD
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
        new_data=request.form['myFile']
        print(new_data)

        data=[1,2,3,4,5,6]

        pdf = FPDF(format='letter')
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.write(5,str(new_data))
        for i in data:
            pdf.write(5,str(i))
            pdf.ln()
        pdf.output("home.pdf")

    return render_template('pay.html')
@app.route('/allowances')
def allowances():
    db = getConnection()
    c = db.cursor()
    try:
        query = c.execute('SELECT * FROM Allowances')
        allowance_rows = query.fetchall()
    except Exception as e:
        c = db.cursor()
        c.execute('''CREATE TABLE  Allowances(Emp_Name VARCHAR(100),Allowance_type VARCHAR(100),Issue_Date DATE,Amount VARCHAR(100))''')
        db.commit()
        return redirect(url_for('allowances'))


    db.close()   
    return render_template('allowances.html',data1=allowance_rows)
@app.route('/add_allowance',methods=('POST','GET'))
def add_allowance():
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
            c.execute('''CREATE TABLE IF NOT EXISTS Allowances(Emp_Name VARCHAR(100),Allowance_type VARCHAR(100),Issue_Date DATE,Amount VARCHAR(100))''')

            c.execute('''INSERT INTO Allowances(Emp_Name,Allowance_type,Issue_Date,Amount)  VALUES {table_values}'''.format(table_values=allowance_data))
            db.commit()
            db.close()
            return redirect(url_for('allowances'))
        except Exception as e:
            raise e

    return render_template('allowances.html')

@app.route('/pay')
def pay():
    db = getConnection()
    c = db.cursor()
    #name,department,date,amount,period
    # query = c.execute('SELECT * FROM Employee_Data')
    # emp_rows = query.fetchall()
    # depart = c.execute('SELECT * FROM Departments')
    # depart_row = depart.fetchall()
    query = c.execute('SELECT * FROM Finances')
    Finance_row = query.fetchall()
    
    return render_template('pay.html',finance=Finance_row)
=======
>>>>>>> bcb8f3bab8c3b1926b461ff4cae29fe37465dcbf
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
   app.run()
