from flask_wtf import FlaskForm
# from flask_login import current_user
from wtforms import StringField,PasswordField,SubmitField, BooleanField,DateField,  SelectField, DateField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo
from nne.models import User, Guarrantor
from flask_login import current_user


class UserRegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=5, max=20, message=('Please enter  your First name and Last name accordingly'))])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20, message=('Please ensure that your Password combination is more than 8 characters'))])
    # role = StringField('Role', validators=[DataRequired(), Length(min=2, max=20)])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=11, max=11,  message=('Invalid or wrong mobile number, check and try again'))])
    gender = SelectField(
        'Gender',
        [DataRequired()],
        choices=[
            ('', 'Select Gender'),
            ('Male', 'Male'),
            ('Female', 'Female')
        ])
    terms = BooleanField ('I accept terms and condition',validators=[DataRequired(1)])
    submit = SubmitField ('Sign Up')
    def validate_phone(self, phone):
        phone_exist = User.query.filter_by(phone = phone.data).first()
        if phone_exist:
            raise ValidationError('This Phone Number already Exist, Kindly use a different one.')

    def validate_email(self, email):
        email_exist = User.query.filter_by(email = email.data).first()
        if email_exist:
            raise ValidationError('This Email address already Exist, Kindly use a different one.')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField ('Request Password Reset')

    def validate_email(self, email):
        email_exist = User.query.filter_by(email = email.data).first()
        if email_exist is None:
            raise ValidationError('Sorry there is no account with that email address. Kindly register')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20, message=('Please ensure that your Password combination is more than 8 characters'))])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField ('Reset Password')



class SearchForm(FlaskForm):

    location= SelectField(
        'location',
        [DataRequired()],
        choices=[
            ('', 'select your state of origin'),
            ('Abia', 'Abia'),
            ('Adamawa', 'Adamawa'),
            ('Akwa Ibom', 'Akwa Ibom'),
            ('Anambra', 'Anambra'),
            ('Bauchi', 'Bauchi'),
            ('Bayelsa', 'Bayelsa'),
            ('Benue', 'Benue'),
            ('Borno', 'Borno'),
            ('Cross River', 'Cross River'),
            ('Delta', 'Delta'),
            ('Ebonyi', 'Ebonyi'),
            ('Edo', 'Edo'),
            ('Ekiti', 'Ekiti'),
            ('Enugu', 'Enugu'),
            ('Gombe', 'Gombe'),
            ('Imo', 'Imo'),
            ('Jigawa', 'Jigawa'),
            ('Kaduna', 'Kaduna'),
            ('Kano', 'Kano'),
            ('Katsina', 'Katsina'),
            ('Kebbi', 'Kebbi'),
            ('Kogi', 'Kogi'),
            ('Kwara', 'Kwara'),
            ('Lagos', 'Lagos'),
            ('Nasarawa', 'Nasarawa'),
            ('Niger', 'Niger'),
            ('Ogun', 'Ogun'),
            ('Ondo', 'Ondo'),
            ('Osun', 'Osun'),
            ('Oyo', 'Oyo'),
            ('Plateau', 'Plateau'),
            ('Rivers', 'Rivers'),
            ('Sokoto', 'Sokoto'),
            ('Taraba', 'Taraba'),
            ('Yobe', 'Yobe'),
            ('Zamfara', 'Zamfara'),
            ('FCT', 'FCT'),
        ])
    role = SelectField(
       'role',
        [DataRequired()],
        choices=[
            ('', 'Select Worker'),
            ('Mid-Wife', 'Mid-Wife'),
            ('Care-giver', 'Care-giver'),
            ('Nursing-Mother', 'Nursing-Mother')
        ]) 
    submit = SubmitField ('Search')



class UserCompleteRegForm(FlaskForm):
    address = StringField('Address', validators=[DataRequired(), Length(min=8, max=250, message=('Please enter  your house Number, street, city, and state accordingly'))])
    id_card = FileField('ID Card', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'jfif'])])

    submit = SubmitField ('Submit')

class ChangeAvatarForm(FlaskForm):
    image = FileField('Change Profile picture', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'jfif'])])
    submit = SubmitField ('Update')

class CaregiverRegistrationForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(min=5, max=20, message=('Please enter  your First name and Last name accordingly'))])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20, message=('Please ensure that your Password combination is more than 8 characters'))])
    role = SelectField(
        'Role',
        [DataRequired()],
        choices=[
            ('', 'Select Worker Type'),
            ('Mid-Wife', 'Mid-Wife'),
            ('Care-giver', 'Care-giver'),
            ('Nursing-Mother', 'Nursing-Mother')
        ])

    phone = StringField('Phone', validators=[DataRequired(), Length(min=11, max=11, message=('Invalid or wrong mobile number, check and try again'))])
    gender = SelectField(
        'Gender',
        [DataRequired()],
        choices=[
            ('', 'Select Gender'),
            ('Male', 'Male'),
            ('Female', 'Female')
        ])
    state_of_origin= SelectField(
        'State of origin',
        [DataRequired()],
        choices=[
            ('', 'select your state of origin'),
            ('Abia', 'Abia'),
            ('Adamawa', 'Adamawa'),
            ('Akwa Ibom', 'Akwa Ibom'),
            ('Anambra', 'Anambra'),
            ('Bauchi', 'Bauchi'),
            ('Bayelsa', 'Bayelsa'),
            ('Benue', 'Benue'),
            ('Borno', 'Borno'),
            ('Cross River', 'Cross River'),
            ('Delta', 'Delta'),
            ('Ebonyi', 'Ebonyi'),
            ('Edo', 'Edo'),
            ('Ekiti', 'Ekiti'),
            ('Enugu', 'Enugu'),
            ('Gombe', 'Gombe'),
            ('Imo', 'Imo'),
            ('Jigawa', 'Jigawa'),
            ('Kaduna', 'Kaduna'),
            ('Kano', 'Kano'),
            ('Katsina', 'Katsina'),
            ('Kebbi', 'Kebbi'),
            ('Kogi', 'Kogi'),
            ('Kwara', 'Kwara'),
            ('Lagos', 'Lagos'),
            ('Nasarawa', 'Nasarawa'),
            ('Niger', 'Niger'),
            ('Ogun', 'Ogun'),
            ('Ondo', 'Ondo'),
            ('Osun', 'Osun'),
            ('Oyo', 'Oyo'),
            ('Plateau', 'Plateau'),
            ('Rivers', 'Rivers'),
            ('Sokoto', 'Sokoto'),
            ('Taraba', 'Taraba'),
            ('Yobe', 'Yobe'),
            ('Zamfara', 'Zamfara'),
            ('FCT', 'FCT'),
        ])
      
    date_of_birth  = DateField('Date of birth', validators=[DataRequired()], format='%Y-%m-%d')
    address = StringField('Address', validators=[DataRequired(), Length(min=8, max=250, message=('Please enter  your house Number, street, city, and state accordingly'))])
    terms = BooleanField ('I accept terms and condition',validators=[DataRequired(1)])
    submit = SubmitField ('Sign Up')
    #This is to check if the phone Number and Email already Exist
    def validate_phone(self, phone):
        phone_exist = User.query.filter_by(phone = phone.data).first()
        if phone_exist:
            raise ValidationError('This Phone Number already Exist, Kindly use a different one.')

    def validate_email(self, email):
        email_exist = User.query.filter_by(email = email.data).first()
        if email_exist:
            raise ValidationError('This Email address already Exist, Kindly use a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField ('Login')

class BioForm(FlaskForm):
    about = TextAreaField('about', validators=[DataRequired(), Length(min=5,  message=('Please give details intro about yourself new *'))])
    marrital_status = SelectField(
        'Marrital Status',
        [DataRequired()],
        choices=[
            ('', 'Select marrital Status'),
            ('Married', 'Married'),
            ('Single', 'Single'),
            ('Divorsed', 'Divorsed'),
            ('Widow', 'Widow')

        ])
    children= SelectField(
        'Number of Kids',
        [DataRequired()],
        choices=[
            ('', 'Select your number of children'),
            ('None', 'None'),
            ('1 Child', '1 Child'),
            ('2 Children', '2 Children'),
            ('3 Children', '3 Children'),
            ('4 Children', '4 Children'),
            ('5 Children', '5 Children'),
            ('6 Children', '6 Children'),
            ('7 Children', '7 Children'),
            ('MSC', '8 Children'),
            ('9 Children', '9 Children'),
            ('10 Children', '10 Children'),
            ('More Than 10 Children', 'More Than 10 Children')
        ])
    education= SelectField(
        'Highest Education Qualification',
        [DataRequired()],
        choices=[
            ('', 'Select your highest qualification'),
            ('None', 'None'),
            ('SSCE', 'SSCE'),
            ('WAEC', 'WAEC'),
            ('GCE', 'GCE'),
            ('NCE', 'NCE'),
            ('OND', 'OND'),
            ('HND', 'HND'),
            ('BSC', 'BSC'),
            ('BEdu', 'BEdu'),
            ('MSC', 'MSC')
        ])
    religion= SelectField(
        'Religion',
        [DataRequired()],
        choices=[
            ('', 'Select your religion'),
            ('None', 'None'),
            ('Christain', 'Christain'),
            ('Muslim', 'Muslim'),
            ('Traditionalist', 'Traditionalist'),
            ('Atheism', 'Atheism'),
            ('Hinduism', 'Hinduism'),
            ('Buddhism', 'Buddhism'),
            ('Judaism', 'Judaism'),
            
        ])
    location= SelectField(
        'Prefered Job location',
        [DataRequired()],
        choices=[
            ('', 'select your current location'),
            ('Abia', 'Abia'),
            ('Adamawa', 'Adamawa'),
            ('Akwa Ibom', 'Akwa Ibom'),
            ('Anambra', 'Anambra'),
            ('Bauchi', 'Bauchi'),
            ('Bayelsa', 'Bayelsa'),
            ('Benue', 'Benue'),
            ('Borno', 'Borno'),
            ('Cross River', 'Cross River'),
            ('Delta', 'Delta'),
            ('Ebonyi', 'Ebonyi'),
            ('Edo', 'Edo'),
            ('Ekiti', 'Ekiti'),
            ('Enugu', 'Enugu'),
            ('Gombe', 'Gombe'),
            ('Imo', 'Imo'),
            ('Jigawa', 'Jigawa'),
            ('Kaduna', 'Kaduna'),
            ('Kano', 'Kano'),
            ('Katsina', 'Katsina'),
            ('Kebbi', 'Kebbi'),
            ('Kogi', 'Kogi'),
            ('Kwara', 'Kwara'),
            ('Lagos', 'Lagos'),
            ('Nasarawa', 'Nasarawa'),
            ('Niger', 'Niger'),
            ('Ogun', 'Ogun'),
            ('Ondo', 'Ondo'),
            ('Osun', 'Osun'),
            ('Oyo', 'Oyo'),
            ('Plateau', 'Plateau'),
            ('Rivers', 'Rivers'),
            ('Sokoto', 'Sokoto'),
            ('Taraba', 'Taraba'),
            ('Yobe', 'Yobe'),
            ('Zamfara', 'Zamfara'),
            ('FCT', 'FCT'),
        ])
    languages = StringField('Languages', validators=[DataRequired(), Length(min=8, max=150, message=('Please enter  the languages you understand '))])
    hobbies = StringField('Hobies', validators=[DataRequired(), Length(min=8, max=150, message=('Please enter  your hobbies'))])
    image = FileField('Prefered status photo', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'jfif'])])
    id_card = FileField('ID Card', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'jfif'])])
    submit = SubmitField ('Submit')

class EditBioForm(FlaskForm):
    about = TextAreaField('about', validators=[DataRequired(), Length(min=1, message=('Please you have a maximum of 180 characters'))])
    marrital_status = SelectField(
        'Marrital Status',
        [DataRequired()],
        choices=[
            ('', 'Select marrital Status'),
            ('Married', 'Married'),
            ('Single', 'Single'),
            ('Divorsed', 'Divorsed'),
            ('Widow', 'Widow')

        ])
    children= SelectField(
        'Number of Kids',
        [DataRequired()],
        choices=[
            ('', 'Select your number of children'),
            ('None', 'None'),
            ('1 Child', '1 Child'),
            ('2 Children', '2 Children'),
            ('3 Children', '3 Children'),
            ('4 Children', '4 Children'),
            ('5 Children', '5 Children'),
            ('6 Children', '6 Children'),
            ('7 Children', '7 Children'),
            ('MSC', '8 Children'),
            ('9 Children', '9 Children'),
            ('10 Children', '10 Children'),
            ('More Than 10 Children', 'More Than 10 Children')
        ])
    education= SelectField(
        'Highest Education Qualification',
        [DataRequired()],
        choices=[
            ('', 'Select your highest qualification'),
            ('None', 'None'),
            ('SSCE', 'SSCE'),
            ('WAEC', 'WAEC'),
            ('GCE', 'GCE'),
            ('NCE', 'NCE'),
            ('OND', 'OND'),
            ('HND', 'HND'),
            ('BSC', 'BSC'),
            ('BEdu', 'BEdu'),
            ('MSC', 'MSC')
        ])
    religion= SelectField(
        'Religion',
        [DataRequired()],
        choices=[
            ('', 'Select your religion'),
            ('None', 'None'),
            ('Christain', 'Christain'),
            ('Muslim', 'Muslim'),
            ('Traditionalist', 'Traditionalist'),
            ('Atheism', 'Atheism'),
            ('Hinduism', 'Hinduism'),
            ('Buddhism', 'Buddhism'),
            ('Judaism', 'Judaism'),
            ('BEdu', 'BEdu'),
            ('MSC', 'MSC')
        ])
    location= SelectField(
        'Prefered Job location',
        [DataRequired()],
        choices=[
            ('', 'select your current location'),
            ('Abia', 'Abia'),
            ('Adamawa', 'Adamawa'),
            ('Akwa Ibom', 'Akwa Ibom'),
            ('Anambra', 'Anambra'),
            ('Bauchi', 'Bauchi'),
            ('Bayelsa', 'Bayelsa'),
            ('Benue', 'Benue'),
            ('Borno', 'Borno'),
            ('Cross River', 'Cross River'),
            ('Delta', 'Delta'),
            ('Ebonyi', 'Ebonyi'),
            ('Edo', 'Edo'),
            ('Ekiti', 'Ekiti'),
            ('Enugu', 'Enugu'),
            ('Gombe', 'Gombe'),
            ('Imo', 'Imo'),
            ('Jigawa', 'Jigawa'),
            ('Kaduna', 'Kaduna'),
            ('Kano', 'Kano'),
            ('Katsina', 'Katsina'),
            ('Kebbi', 'Kebbi'),
            ('Kogi', 'Kogi'),
            ('Kwara', 'Kwara'),
            ('Lagos', 'Lagos'),
            ('Nasarawa', 'Nasarawa'),
            ('Niger', 'Niger'),
            ('Ogun', 'Ogun'),
            ('Ondo', 'Ondo'),
            ('Osun', 'Osun'),
            ('Oyo', 'Oyo'),
            ('Plateau', 'Plateau'),
            ('Rivers', 'Rivers'),
            ('Sokoto', 'Sokoto'),
            ('Taraba', 'Taraba'),
            ('Yobe', 'Yobe'),
            ('Zamfara', 'Zamfara'),
            ('FCT', 'FCT'),
        ])
    languages = StringField('Languages', validators=[DataRequired(), Length(min=8, max=150, message=('Please enter  the languages you understand '))])
    hobbies = StringField('Hobies', validators=[DataRequired(), Length(min=8, max=150, message=('Please enter  your hobbies'))])
    submit = SubmitField ('Submit')


class GuarrantorForm(FlaskForm):

    guarrantor_one_name = StringField('Guarrantor One Name', validators=[DataRequired(), Length(min=8, max=150, message=('Please enter  your First name and Last name accordingly'))])
    guarrantor_two_name = StringField('Guarrantor Two Name', validators=[DataRequired(), Length(min=8, max=150, message=('Please enter  your First name and Last name accordingly'))])
    guarrantor_one_phone = StringField('Guarrantor One Phone', validators=[DataRequired(),Length(min=11, max=11,  message=('Invalid or wrong mobile number, check and try again'))])
    guarrantor_two_phone = StringField('Guarrantor Two Phone', validators=[DataRequired(),Length(min=11, max=11,  message=('Invalid or wrong mobile number, check and try again'))])
    guarrantor_one_address = StringField('Guarrantor One Address', validators=[DataRequired(), Length(min=8, max=250, message=('Please enter  your house Number, street, city, and state accordingly'))])
    guarrantor_two_address = StringField('Guarrantor Two Address', validators=[DataRequired(), Length(min=8, max=250, message=('Please enter  your house Number, street, city, and state accordingly'))])
    guarrantor_one_id_card = FileField('Guarrantor One ID Card', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'jfif'])])
    guarrantor_two_id_card = FileField('Guarrantor Two ID Card', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'jfif'])])
    submit = SubmitField ('Submit')
    # def validate_email(self, worker_email):
    #     email_exist = Guarrantor.query.filter_by(worker_email = worker_email.data).first()
    #     if email_exist:
    #         raise ValidationError('Please note that Guarrantors details has been supplied, awaiting admin Verification. contact admin at admin@mama.com')

class PaymentForm(FlaskForm):
    bank_name= SelectField(
        'Bank Name',
        [DataRequired()],
        choices=[
            ('', 'Select your bank'),
            ('None', 'None'),
            ('FCMB', 'FCMB'),
            ('First bank of Nigeria', 'First bank of Nigeria'),
            ('Fidelity Bank', 'Fidelity Bank'),
            ('GtBank Plc', 'GtBank Plc'),
            ('Union Bank', 'Union Bank'),
            ('Jaiz Bank', 'Jaiz Bank'),
            ('United Bank For Africa', 'United Bank For Africa'),
            ('Wema Bank', 'Wema Bank'),
            ('Zenith Bank Plc', 'Zenith Bank Plc')
        ])
    bank_account_number = StringField('Bank Account Number', validators=[DataRequired(), Length(min=8, max=10, message=('Please enter a valid bank account Number'))])
    bank_account_name = StringField('Bank Account Name', validators=[DataRequired(), Length(min=8, max=150, message=('Please enter  your First name and Last name accordingly'))])
    submit = SubmitField ('Submit')