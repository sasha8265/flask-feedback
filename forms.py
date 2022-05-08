from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

    

 
class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired()])

    # def __init__(self):
    #     FlaskForm.__init__(self)
    #     self.user = None

    # def validate(self):
    #     reg_val = FlaskForm.validate(self)
    #     if not reg_val:
    #         return False

    #     user = User.query.filter_by(username=self.username.data).first()
    #     email = User.query.filter_by(email=self.email.data).first()

    #     if user is not None:
    #         self.username.errors.append('username already in use')
    #         return False
        
    #     if email is not None:
    #         self.email.errors.append('email address already in use')
    #         return False

    #     self.user = user
    #     return True    
