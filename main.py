from flask import Flask, render_template, url_for, request
from flaskwebgui import FlaskUI  # get the FlaskUI class
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import TextField, SubmitField, TextAreaField
from wtforms.validators import  Length, Email, Required
app = Flask(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
Bootstrap(app)
# Feed it the flask app instance (check bellow what param you can add)
ui = FlaskUI(app)
# do your logic as usual in Flask
@app.route("/",methods=['GET','POST'])
def index():
    form=CreateDataBaseForm(request.form)
    return render_template('admin_dashboard.html',form=form)

class CreateDataBaseForm(FlaskForm):
    database_name = TextField('Enter name of the database', validators=[Required(), Email()])
    submit = SubmitField('Create')
# call the 'run' method

ui.run()
