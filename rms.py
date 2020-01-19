import base64
import datetime
from datetime import datetime
import io
from io import BytesIO
import os

from requests import session
from sqlalchemy.orm import load_only
import numpy as np
from PIL import Image

from flask import Flask, render_template, url_for, request,jsonify,redirect,g,send_file,Response,flash
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
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
autoflush=True
db  = SQLAlchemy(app)


class Data(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    company_name = db.Column(db.String(300))
    Tin_number = db.Column(db.String(300))
    nssf_number = db.Column(db.String(300))
    address = db.Column(db.String(300))
    email = db.Column(db.String(300))
    telephone = db.Column(db.String(300))
    image=db.Column(db.LargeBinary)
    def __init__(self,company_name,Tin_number,nssf_number,address,email,telephone,image):
        self.company_name=company_name
        self.Tin_numer=Tin_number
        self.nssf_number=nssf_number
        self.address=address
        self.email=email
        self.telephone=telephone
        self.image=image
db.create_all()
db.session.commit()


class Employee_Data(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    Emp_ID =db.Column(db.String(300))
    Tin_Number = db.Column(db.String(300))
    Nssf_Number = db.Column(db.String(300))
    Designation=db.Column(db.String(300))
    Employee_Status = db.Column(db.String(300))
    Residence_type=db.Column(db.String(20))
    Joining_Date = db.Column(db.String(300))
    End_of_Contract = db.Column(db.String(300))
    Firstname =db.Column(db.String(300))
    Lastname = db.Column(db.String(300))
    DOB=db.Column(db.String(300))
    Marital_Status=db.Column(db.String(300))
    Gender =db.Column(db.String(300))
    Nationality = db.Column(db.String(300))
    Current_Address=db.Column(db.String(300))
    Mobile = db.Column(db.String(300))
    Home_Phone = db.Column(db.String(300))
    Email = db.Column(db.String(300))
    Account_Name = db.Column(db.String(300))
    Account_Number =db.Column(db.String(300))
    Bank_Name=db.Column(db.String(300))
    Bank_Branch = db.Column(db.String(300))
    Attendance_Status = db.Column(db.String(300))
    Level_of_Education = db.Column(db.String(300))
    Institution = db.Column(db.String(300))
    Cv=db.Column(db.LargeBinary)
    Gross_Pay = db.Column(db.String(300))
    Next_of_Kin = db.Column(db.String(300))
    Supervisor=db.Column(db.String(300))
    Department=db.Column(db.String(300))
    def __init__(self,Emp_ID,Tin_Number,Nssf_Number,Designation,Employee_Status,Joining_Date,End_of_Contract,Firstname,
                 Lastname,DOB,Marital_Status,Residence_type,Gender,Nationality,Current_Address,Mobile,
                 Home_Phone,Email,Account_Name,Account_Number,Bank_Name,Bank_Branch,Attendance_Status,
                 Level_of_Education,Institution,Cv,Gross_Pay,Next_of_Kin,Supervisor,Department):
        self.Emp_ID=Emp_ID
        self.Tin_Number=Tin_Number
        self.Nssf_Number=Nssf_Number
        self.Designation=Designation
        self.Employee_Status=Employee_Status
        self.Residence_type=Residence_type
        self.Joining_Date=Joining_Date
        self.End_of_Contract=End_of_Contract
        self.Firstname=Firstname
        self.Lastname=Lastname
        self.DOB=DOB
        self.Marital_Status=Marital_Status
        self.Gender=Gender
        self.Nationality=Nationality
        self.Current_Address=Current_Address
        self.Mobile=Mobile
        self.Home_Phone=Home_Phone
        self.Email=Email
        self.Account_Name=Account_Name
        self.Account_Number=Account_Number
        self.Bank_Name=Bank_Name
        self.Bank_Branch=Bank_Branch
        self.Attendance_Status=Attendance_Status
        self.Level_of_Education=Level_of_Education
        self.Institution=Institution
        self.Cv=Cv
        self.Gross_Pay=Gross_Pay
        self.Next_of_Kin=Next_of_Kin
        self.Supervisor=Supervisor
        self.Department=Department
db.create_all()
db.session.commit()
#creating a db to the database
DATABASE  = 'Database.db'


def getConnection():
    con = getattr(g,'_database',None)
    if con is None:
        con = g._database = sqlite3.connect(DATABASE)
    return con

def image():
    try:
        file = Data.query.filter_by(id=1).first()
        imgs = base64.b64encode(file.image).decode('ascii')
    except:
        imgs = "User"
    return imgs
imgs=image()

def add_data(emp_id,name,gross_pay,residence):
    #a list for adding data into the finance module
    detail=[]
    db = getConnection()
    c = db.cursor()
    detail.append(emp_id)
    detail.append(name)
    detail.append(float(gross_pay))
    #calculate NSSf contribution
    #5% calculation
    employee_contrnssf=0.05*float(gross_pay)
    detail.append(float(employee_contrnssf))
    #employer NSSf contribution
#    app.run( )

    employeer_contrnssf=0.1*float(gross_pay)
    detail.append(float(employeer_contrnssf))
    nssf_contribution = employee_contrnssf+employeer_contrnssf
    detail.append(nssf_contribution)

    #calculate payee
        
    if residence=='Resident':
        #Paye for residents
        if float(gross_pay)<235000:
            paye=0
                    
        elif float(gross_pay) in range(235000,335000):
            paye=0.1*float(gross_pay)
                    
        elif float(gross_pay) in range(335000,410000):
            paye=10000 + 0.2*float(gross_pay)
                    
        elif float(gross_pay)>410000:
            paye=25000+0.3*float(gross_pay)
                    
        elif float(gross_pay)>10000000:
            paye=25000+0.3*float(gross_pay)+0.1*float(gross_pay)
                    
        else:
            print("Enter valid money for the employeee")

    elif residence== 'Non-Resident':
        #paye for non residents
        if float(gross_pay)<335000:
            paye=0.1*float(gross_pay)
                    
        elif float(gross_pay) in range(335000,410000):
            paye=33500 + 0.2*float(gross_pay)
                    
        elif float(gross_pay)>410000:
            paye=48500+0.3*float(gross_pay)
                    
        elif float(gross_pay)>10000000:
            paye=48500+0.3*float(gross_pay)+0.1*float(gross_pay)
                    
        else:
            print("Enter valid money for the employeee")


    else:
        print("warning this field is required !!!")
    detail.append(paye)
    tt_deductions=paye+nssf_contribution
    detail.append(tt_deductions)
    Net_salary=float(gross_pay)-tt_deductions
    detail.append(Net_salary)
            
    arr=[str(i) for i in detail]
    detail_data = tuple(arr)
    c.execute('''Insert INTO Finances(Emp_ID,Employee_Name,Gross_pay,employee_contrb,employer_contrb,nssf_contrib,Paye,Total_Dect,Net_pay) VALUES {table_value}'''.format(table_value=detail_data))
            
    db.commit()
    db.close()
    
    
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
        try:
            new_file = Data(company_name=Company_name, Tin_number=tin,
                            nssf_number=c_nssf_num, address=c_address,
                            email=c_email, telephone=c_Tel, image=img)
            db.session.add(new_file)
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            raise e
    return render_template('index.html')


@app.route('/',methods=['POST','GET'])
def index():
    return render_template('index.html',img=imgs)

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
    return  render_template('edit.html',cname=cname,tin=tin,nssf=nssf,address=address,email=email,tel=tel,img=imgs)
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
    # file = Data.query.filter_by(id=1).first()
    # img = base64.b64encode(file.image).decode('ascii')
    image()
    db = getConnection()
    c = db.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Departments(Department VARCHAR(100) UNIQUE)''')
    # query1 = c.execute('SELECT  Department ,COUNT(Employee_name) FROM Roles GROUP BY Department')
    query = c.execute('SELECT  Department FROM  Departments')
    rows = query.fetchall()
    db.commit()
    db.close()
    return render_template('department.html',rows=rows,img=imgs)
@app.route('/Employee')
def Employee():
    #connecting and selecting departments
    db=getConnection()
    c=db.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Finances(Emp_ID VARCHAR(15),Employee_Name VARCHAR(100),Gross_pay VARCHAR(100),employee_contrb VARCHAR(100),employer_contrb VARCHAR(100),nssf_contrib VARCHAR(50),Paye VARCHAR(100),Total_Dect VARCHAR(100),Net_pay VARCHAR(100))''')
    query = c.execute('SELECT * FROM  Departments')
    rows = query.fetchall()
    db.commit()
    db.close()
    return render_template('employe_maintence.html',rows=rows,img=imgs)
@app.route('/add_employee',methods=['POST','GET'])
def add_employee():
    
    # file = Data.query.filter_by(id=1).first()
    # img = base64.b64encode(file.image).decode('ascii')
    if request.method == 'POST':
        emp_id=request.form['emp_id']
        tin_num=request.form['tin_num']
        nssf_num=request.form['nssf_num']
        designation=request.form['designation']
        status=request.form['status']
        residence=request.form['residence_nature']
        join_date=request.form['join_date']
        end_date=request.form['end_date']
        first_name=request.form['first_name']
        last_name=request.form['last_name']
        name=first_name+" "+last_name
        date_of_birth=request.form['date_of_birth']
        marital_status=request.form['marital_status']
        gender=request.form['gender']
        nationality=request.form['nationality']
        current_address=request.form['current_address']
        mobile=request.form['mobile']
        phone=request.form['phone']
        email=request.form['email']
        account_name=request.form['account_name']
        account_number=request.form['account_number']
        bank_name=request.form['bank_name']
        bank_branch=request.form['bank_branch']
        sts=request.form['sts']
        level=request.form['level']
        institution=request.form['instition']
        cv=request.files['cv']
        file=cv.read()
        gross_pay=request.form['gross_pay']
        
        next_of_kin=request.form['next_of_kin']
        supervisor=request.form['supervisor']
        department=request.form['department']
        try:
            new_file = Employee_Data(Emp_ID=emp_id,Tin_Number=tin_num,Nssf_Number=nssf_num,Designation=designation,Employee_Status=status,Residence_type=residence,Joining_Date=join_date,
                                     End_of_Contract=end_date,Firstname=first_name,Lastname=last_name,DOB=date_of_birth,Marital_Status=marital_status,Gender=gender,
                                     Nationality=nationality,Current_Address=current_address,Mobile=mobile,Home_Phone=phone,Email=email,Account_Name=account_name,Account_Number=account_number,
                                     Bank_Name=bank_name,Bank_Branch=bank_branch,Attendance_Status=sts,Level_of_Education=level,Institution=institution,
                                     Cv=file,Gross_Pay=gross_pay,Next_of_Kin=next_of_kin,Supervisor=supervisor,Department=department)
            db.session.add(new_file)
            add_data(emp_id,name,gross_pay,residence)
            db.session.commit()
            
            # #adding data to the finance module
            # db=getConnection()
            # c=db.cursor()

            
            return redirect(url_for('Employee_list'))
        except Exception as e:
            raise e
    return render_template('employe_maintence.html',img=imgs)
####leave and attendance
@app.route('/Leave')
def Leave():
    users = Employee_Data.query.all()
    return render_template('leave.html',sql_rows=users,img=imgs)
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
            return  redirect(url_for('Leave'))
        except Exception as e:
            raise e
    return render_template('leave.html',img=imgs)
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
    return render_template('leave.html',img=imgs)
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
    return render_template('leave.html',img=imgs)
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
    return  render_template('working_days.html',img=imgs)
##employee list
@app.route('/Employee_list',methods=['POST','GET'])
def Employee_list():
    users = Employee_Data.query.all()
    # t = db.cursor()
    # sql = t.execute('''SELECT Employee_name,Role,Department FROM Roles''')
    # sql_row = sql.fetchall()
    # for i, x in zip(sql_row,rows):
    #     data = i + x
    #     df.append(data)
    return render_template('employee_list.html',users=users,img=imgs)
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
        try:
            query_update=Employee_Data.query.filter_by(Firstname=name).first()
            query_update.Attendance_Status='Inactive'
            db.session.commit()
            return  redirect(url_for('Employee_list'))
        except Exception as e:
            raise e
    return render_template('employee_list.html.html')
##department list
@app.route('/Department_list',methods=['POST','GET'])
def Department_list():
    error = None
    if request.method=='POST':
        departments=request.form['departments']
        db=getConnection()
        c=db.cursor()
        query =c.execute("""SELECT Department FROM Departments WHERE Department ='{dn}' """.format(dn=departments))
        data =query.fetchone()
        try:
            if data:
                message = "Department exists"
                flash(message)
            else:
                c.execute("Insert INTO Departments(Department) VALUES('{tbv}')".format(tbv=departments))
                error = 'Successfully inserted'
                db.commit()
                db.close()
            return redirect(url_for('department'))
        except Exception as e:
                raise e
    return render_template('department.html',img=imgs)

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
            return redirect(url_for('department'))
        except Exception as e:
            raise e
    return  render_template('department_list.html')
##attendance
@app.route('/Attendance',methods=['POST','GET'])
def Attendance():
    users = Employee_Data.query.all()
    # file = Data.query.filter_by(id=1).first()
    # img = base64.b64encode(file.image).decode('ascii')
    return render_template('attendance.html',rows=users,img=imgs)
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
    # file = Data.query.filter_by(id=1).first()
    # img = base64.b64encode(file.image).decode('ascii')
    try:
        query = c.execute('SELECT * FROM Finances')
        sql_rows = query.fetchall()
    except Exception as e:
        raise e
    
    return render_template('salary.html',data1=sql_rows,img=imgs)

##employee salaries
@app.route('/Salaries')
def Salaries():
    db = getConnection()
    c = db.cursor()
    try:
        gallowances = c.execute('SELECT * FROM Allowances')
        rallowances = gallowances.fetchall()
        gpayment = c.execute('SELECT * FROM Payment')
        rpay_list = gpayment.fetchall()
    except:
        c = db.cursor()
        # creat allowances table is not existing
        c.execute(
            '''CREATE TABLE IF NOT EXISTS Allowances(Emp_Name VARCHAR(100),Allowance_type VARCHAR(100),Issue_Date DATE,Amount VARCHAR(100))''')
        c.execute(
            '''CREATE TABLE IF NOT EXISTS Payment(Emp_ID VARCHAR(100),Salary VARCHAR(15),Paid_month VARCHAR(15),pYear VARCHAR(10),Issue_Date DATE)''')
        return redirect(url_for('Salaries'))
    # file = Data.query.filter_by(id=1).first()
    # img = base64.b64encode(file.image).decode('ascii')
    return render_template('Salaries.html',rallowances=rallowances,rpay_list=rpay_list,img=imgs)

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
        other=c.execute('''SELECT * FROM Deduction WHERE Emp_ID=('{nd}')'''.format(nd=new_data))
        rother =  other.fetchall()
        emdata = c.execute('''SELECT * FROM employee__data WHERE Emp_ID=('{nd}')'''.format(nd=new_data))
        rdata =  emdata.fetchall()
        crows=Data.query.all()
        for i in crows:
            cname = i.company_name
            caddress=i.address
        gallowances = c.execute('''SELECT * FROM Allowances WHERE Emp_ID=('{nd}')'''.format(nd=new_data))
        rallowances =  gallowances.fetchall()
        gpayment = c.execute('''SELECT * FROM Payment WHERE Emp_ID=('{name}')'''.format(name=new_data))
        rpay_list = gpayment.fetchall()
        gf = c.execute('''SELECT * FROM Finances WHERE Emp_ID=('{name}')'''.format(name=new_data))
        rf_list = gf.fetchall()
         #total deductions 
        dsum=c.execute('''SELECT SUM(Amount) FROM Deduction WHERE Emp_id=('{name}')'''.format(name=new_data))
        drow = dsum.fetchall()
        valuer=float(drow[0][0])
        # total payment
        netcal=c.execute('''SELECT Net_pay FROM Finances WHERE Emp_ID=('{name}')'''.format(name=new_data))
        nets=netcal.fetchall()
        # comp = nets - drow[0][0]
        netpay=float(nets[0][0])-valuer

        pdf = FPDF(format='letter')
        pdf.add_page()
        col_width =100
        th =10
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(200, 5,cname,align="C")
        pdf.ln()
        pdf.multi_cell(200, 5,caddress,align="C")
        pdf.ln()
        pdf.multi_cell(200, 5, 'Monthly Payslip',align="C")
        pdf.ln()
        pdf.multi_cell(0, 5, ('Employee Name: %s' % rf_list[0][1]))
        pdf.ln()
        pdf.multi_cell(0, 5, ('Designation: %s' % rdata[0][4]))
        pdf.ln()
        pdf.multi_cell(0, 5, ('Designation: %s' % rpay_list[0][4]))
        pdf.ln()
        pdf.multi_cell(200, 5, 'Allowances',align="C")
        pdf.ln()
        for row in rallowances:
            pdf.cell(col_width, th, str(row[1]), border=1)
            pdf.cell(col_width, th, row[2], border=1)
            pdf.cell(col_width, th, row[3], border=1)
            pdf.ln(10)
        pdf.ln(5)
        pdf.multi_cell(200, 5, 'Deductions And Net Pay',align="C")
        pdf.ln(5)
        pdf.multi_cell(0, 5, ('Other deduction: %s' % valuer ),align="C")
        pdf.ln()
        for drow in rf_list :
           pdf.cell(col_width, th, "Nssf Contribution", border=1)
           pdf.cell(col_width, th, drow[4], border=1)
           pdf.ln(10)
           pdf.cell(col_width, th, "PAYE", border=1)
           pdf.cell(col_width, th, drow[5], border=1)
           pdf.ln(10)
           pdf.cell(col_width, th, "Gross Pay", border=1)
           pdf.cell(col_width, th, drow[2], border=1)
           pdf.ln(10)
           pdf.ln(10)
           pdf.cell(col_width, th, "Net pay", border=1)
           pdf.cell(col_width, th, drow[8], border=1)
           pdf.ln(10)
           
        pdf.ln(5)
        pdf.multi_cell(0, 5, ('Salary: %s' % netpay ))
        pdf.ln()
        


        # pdf.output("home.pdf")
    # return Response(pdf.output(dest='S'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=pay_slip.pdf'})
    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=pay_slip.pdf'})
@app.route('/allowances')
def allowances():
    db = getConnection()
    c = db.cursor()
    # file = Data.query.filter_by(id=1).first()
    # img = base64.b64encode(file.image).decode('ascii')
    try:
        #select employe name from employee table
        serows=Employee_Data.query.all()
        #select allowance type from allowance type table
        atype = c.execute('SELECT * FROM Allowance_types')
        arows = atype.fetchall()
        #select allownaces
        query = c.execute('SELECT * FROM Allowances')
        allowance_rows = query.fetchall()
    except Exception as e:
        c = db.cursor()
        #creat allowances table is not existing
        c.execute('''CREATE TABLE IF NOT EXISTS Allowances(Emp_ID VARCHAR(100),Allowance_type VARCHAR(100),Issue_Date DATE,Amount VARCHAR(100))''')
        #create employee table is not exist
        #create allowance type  table is not exist
        c.execute('''CREATE TABLE IF NOT EXISTS Allowance_types(Allowance_id VARCHAR(100),Allowance_type VARCHAR(100),Creation_Date DATE)''')
        db.commit()
        return redirect(url_for('allowances'))
    return render_template('allowances.html',data1=allowance_rows,arows=arows,serows=serows,img=imgs)
@app.route('/add_allowance',methods=('POST','GET'))
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
            c.execute('''INSERT INTO Allowances(Emp_ID,Allowance_type,Issue_Date,Amount)  VALUES {table_values}'''.format(table_values=allowance_data))
            db.commit()
            db.close()
            return redirect(url_for('allowances'))
        except Exception as e:
            raise e

    return render_template('allowances.html',img=imgs)

@app.route('/deductions')
def deductions():
    db = getConnection()
    c = db.cursor()
    try:
        #select employe name from employee table
        serows=Employee_Data.query.all()
        #select allowance type from allowance type table
        dtype = c.execute('SELECT * FROM Deduction_types')
        drows = dtype.fetchall()
        #select allownaces
        query = c.execute('SELECT * FROM  Deduction')
        adeduction_rows = query.fetchall()
       
    except:
        c = db.cursor()
        #creat allowances table is not existing
        c.execute('''CREATE TABLE IF NOT EXISTS Deduction(Emp_id VARCHAR(15),deduction_type VARCHAR(100),Issue_Date DATE,Amount VARCHAR(100))''')
        #create employee table is not exist
        #create allowance type  table is not exist
        c.execute('''CREATE TABLE IF NOT EXISTS Deduction_types(Dect_id VARCHAR(100),Deduction_type VARCHAR(100),Description VARCHAR(100),Creation_Date DATE)''')
        db.commit()
        return redirect(url_for('deductions'))


    db.close()
    return render_template('deductions.html',adeduction_rows=adeduction_rows,drows=drows,serows=serows,img=imgs)
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
            c.execute('''INSERT INTO Deduction(Emp_id,deduction_type,Issue_Date,Amount)  VALUES {table_values}'''.format(table_values=edd_data))
            db.commit()
            return redirect(url_for('deductions'))
        except Exception as e:
            raise e
    return render_template('deductions.html',img=imgs)
#NSSF submission
@app.route('/nssf')
def nssf():
    return render_template('nssf_subf.html',img=imgs)
@app.route('/nssf_sub',methods=['POST','GET'])
def nssf_sub():
    if request.method=='POST':
        syear=request.form['year']
        submonth=request.form['sMonth']
        
        db = getConnection()
        c = db.cursor()
        # company_details=c.execute('SELECT * FROM  Artistry')
        crows =Data.query.all()
        for i in crows:
            cname=i.company_name
            nssf_number=i.nssf_number
        ford=c.execute("""SELECT  employee__data.Emp_ID,
        employee__data.Emp_ID,employee__data.Nssf_Number,
        employee__data.Residence_type,Finances.Employee_Name,
        Finances.Gross_pay,Finances.employee_contrb,Finances.employer_contrb,
        Finances.nssf_contrib,employee__data.Mobile FROM Payment JOIN Finances ON(Payment.Emp_ID=Finances.Emp_ID) JOIN employee__data ON(Payment.Emp_ID= employee__data.Emp_ID) WHERE Payment.Paid_month=('{nmonth}') AND  Payment.pYear=('{yr}')"""
                       .format(nmonth=submonth,yr=syear))
        drows = ford.fetchall()
        print(drows)
        #sum
        tsum=c.execute("select SUM(Finances.Total_Dect)from Payment JOIN Finances ON(Payment.Emp_ID=Finances.Emp_ID) JOIN employee__data ON(Payment.Emp_ID= employee__data.Emp_ID) WHERE Payment.Paid_month=('{nmonth}')".format(nmonth=submonth))
        tsumval = tsum.fetchall()
        
        output=BytesIO()
        
        workbook = xlsxwriter.Workbook(output)
       #writing excel headers
        worksheet = workbook.add_worksheet()
        cell_format = workbook.add_format()
     #create a format to use in the merged range
        cell_format.set_font_color('Sliver')
        coname=cname
        nssf=nssf_number
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
        #go back to the beginning of the stream
        output.seek(0)
        
  
    
    # return redirect(url_for('nssf'))
    return send_file(output, attachment_filename="nssf.xlsx", as_attachment=True)

@app.route('/pay')
def pay():
    # file = Data.query.filter_by(id=1).first()
    # img = base64.b64encode(file.image).decode('ascii')
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
        c.execute('''CREATE TABLE IF NOT EXISTS Payment(Emp_ID VARCHAR(100),Salary VARCHAR(15),Paid_month VARCHAR(15),pYear VARCHAR(10),Issue_Date DATE)''')
        db.commit()
        return redirect(url_for('pay'))
        
    
    return render_template('pay.html',pay_list=dpay_list,Finance=depart_row,img=imgs)
    
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
            c.execute('''INSERT INTO Payment(Emp_ID,Salary,Paid_month,pYear,Issue_Date)  VALUES {table_value}'''.format(table_value=main_add))
            db.commit()
            db.close()
            return redirect(url_for('pay'))
        except Exception as e:
            raise e

    return render_template('pay.html',img=imgs)

@app.route('/settings',methods=['POST','GET'])
def settings():
    db = getConnection()
    c = db.cursor()
    d=db.cursor()
    # file = Data.query.filter_by(id=1).first()
    # img = base64.b64encode(file.image).decode('ascii')
    users = Employee_Data.query.all()
    try:
        query = c.execute('SELECT * FROM Roles')
        rows = query.fetchall()
        depart = d.execute('SELECT Department FROM Departments')
        depart_row = depart.fetchall()
    except:
        c.execute(
            '''CREATE TABLE IF NOT EXISTS Roles(Employee_name VARCHAR(100),Role VARCHAR(100),Password VARCHAR(100),Department VARCHAR(100))''')
        db.commit()
        return redirect('settings')
    db.close()
    return render_template('settings.html',rows=rows,sql_rows=users,depart_row=depart_row,img=imgs)
##Assigning employees roles
@app.route('/Role',methods=['POST','GET'])
def Role():
    if request.method=='POST':
        name=request.form['name']
        role=request.form['role']
        password=request.form['password']
        department=request.form['department']
        try:
            db = getConnection()
            c = db.cursor()
            c.execute("""INSERT INTO Roles(Employee_name,Role,Password,Department) VALUES('{name}','{role}','{password}','{department}')""".
                      format(name=name,role=role,password=password,department=department))
            db.commit()
            db.close()
            return redirect(url_for('settings'))
        except Exception as e:
            raise e
    return render_template('settings.html',img=imgs)
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
    return render_template('settings.html',img=imgs)
if __name__ == "__main__":

   app.run( )

#    app.run(debug=True)
#    app.run( )


