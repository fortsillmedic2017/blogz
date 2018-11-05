from flask_wtf import FlaskForm, form
from wtforms import fields, Form, HiddenField,StringField, IntegerField,  PasswordField, SubmitField, BooleanField, Form, TextField, TextAreaField, validators
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired, Optional, Regexp
from wtforms_sqlalchemy.fields import QuerySelectField

class Add_Blog(FlaskForm):
    heading = StringField("The title for your new blog:", 
              validators=[DataRequired(),Length(min=2, max=250, message="That's not a valid title.")])
    body = TextAreaField("Your new blog:", validators=[DataRequired(), 
           Length(min=2, max=5000, message="That's not a valid message.")])
    hidden = HiddenField()
    
#==============================================================================
class UserSignup(FlaskForm):
    username = StringField("Username", validators=[Length(
        min=3, max=20, message="That's not a valid username.")])
   
    password = PasswordField("Password",
                             validators=[Length(min=3, max=20, message="That's not a valid password. Must have at lease 3 characters"), EqualTo("verify_password", message="Your passwords did not match.")])

    verify_password = PasswordField("Verify Password",
                                    validators=[Length(min=3, max=20, message="That's not a valid password. Must have at lease 3 characters"),
                                                EqualTo("password", message="Your passwords did not match.")])

    email = StringField("Email", validators=[Email()])
    
    hidden = HiddenField()

    remember = BooleanField("Remember Me")



#==========in puts for Login Form for main.py  =========================>
class UserLogin(FlaskForm):
    username = StringField("Username", validators=[InputRequired(),Length(
        min=3, max=20, message="That's not a valid username.")])
  
    password = PasswordField("Password",
                             validators=[InputRequired(),Length(min=3, max=20, message="That's not a valid password. Must have at lease 3 characters")])

    
