from flask import Flask, render_template, redirect, url_for, flash,abort
from flask_bootstrap import Bootstrap
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask_wtf import FlaskForm
from sqlalchemy.sql.expression import all_
from wtforms import StringField, SubmitField
from wtforms.fields.core import DateTimeField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] =os.environ.get("DATABASE_URI",'sqlite:///people.db') 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

Bootstrap(app)

class person(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    age = StringField("Age",validators=[DataRequired()])
    submit = SubmitField("Add")


class Search(FlaskForm):
    name = StringField("Name")
    last_name = StringField("Last Name")
    age = StringField("Age")
    submit = SubmitField("Search")


class People(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(250),nullable=False)
  last_name = db.Column(db.String(250),nullable=False)
  age = db.Column(db.Integer,nullable=False)
  date_time = db.Column(db.DateTime,default=datetime.datetime.now,nullable=False)

#db.create_all()

@app.route("/")
def home():
    person_form = person()
    search_form = Search()
    all_person= People.query.all()
    return render_template("Index.html", person_form=person_form, search_form=search_form,data=all_person)



@app.route("/add_data",methods=["GET","POST"])
def add_data():
    person_form = person()
    search_form = Search()
    if person_form.validate_on_submit() and person_form.submit.data:
        
        new_person = People(
            name=person_form.name.data,
            last_name=person_form.last_name.data,
            age =person_form.age.data,
             )
        db.session.add(new_person)
        db.session.commit()
        return redirect(url_for("home"))
   
    return render_template("Index.html", person_form=person_form, search_form=search_form)

@app.route("/show_data",methods=["POST"])
def show_data():
     person_form = person()
     search_form = Search()
     if search_form.validate_on_submit() and search_form.submit.data:
            name=search_form.name.data
            last_name=search_form.last_name.data
            age =search_form.age.data
           
            all_person= People.query.filter(or_(People.name.like(name),
                                            People.last_name.like(last_name),People.age.like(age)))
            return render_template("Index.html",data=all_person,person_form=person_form, search_form=search_form)
     
     return render_template("Index.html", person_form=person_form, search_form=search_form)
   

if __name__ == '__main__':
     app.run(debug=True)
    
