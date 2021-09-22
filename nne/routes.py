import os
import random
import secrets
from flask import render_template, request, session, logging, url_for, redirect, flash, request
from nne import app, db, bcrypt, mail
from nne.forms import UserRegistrationForm, CaregiverRegistrationForm, LoginForm,SearchForm, UserCompleteRegForm, ChangeAvatarForm, BioForm,EditBioForm, GuarrantorForm, PaymentForm, RequestResetForm, ResetPasswordForm
from nne.models import Users, User, Workers, Guarrantor, Payment
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

# Setup Flask-Security
# user_datastore = SQLAlchemyUserDatastore(db, User, Role)
# security = Security(app, user_datastore)

# this is the default welcome page route
@app.route('/')
def index():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  return render_template('/index.html')

# This is the home page route
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
  form = SearchForm()
  if form.validate_on_submit():
    page = request.args.get('page', 1, type=int)
    givers= Workers.query.filter_by(role= form.role.data, location= form.location.data).order_by(Workers.completed_at.desc()).paginate(page = page,  per_page=3)
    if givers:
      return render_template('/home.html', title='Search', givers = givers, form=form)
    else:
      return 'No recent found'
      
  else:
    page = request.args.get('page', 1, type=int)
    workers = Workers.query.order_by(Workers.completed_at.desc()).paginate(page = page,  per_page=3)
    return render_template('/home.html', title='home', workers = workers, form=form)

# This is the detail page for the newly verified caregivers
@app.route('/details/<int:care_id>')
@login_required
def detail(care_id):
  workers= Workers.query.get_or_404(care_id)
  return render_template('/details.html',  workers = workers)

# This is the detail page for the newly verified caregivers
@app.route('/account')
@login_required
def acco():
  workers = Workers.query.filter_by(email = current_user.email)
  image = url_for('static', filename='user_uploads/' + str(current_user.image))
  return render_template('/account.html', title='Account', image=image, workers = workers)    

# This is the change role infor page route
@app.route('/changeRoleInfo')
@login_required
def changeInfor():
   image = url_for('static', filename='user_uploads/' + str(current_user.image))
   return render_template('/changeRoleInfo.html', title='Change Role', image= image)


# This is the recent page route
@app.route('/recent' , methods=['GET', 'POST'])
@login_required
def recent():
  image = url_for('static', filename='user_uploads/' + str(current_user.image))
  return render_template('/recent.html', title='Recent History', image= image)

@app.route('/avarter' , methods=['GET', 'POST'])
@login_required
def avartar():
   form = ChangeAvatarForm()
   if form.validate_on_submit():
    if form.image.data:
      picture_file = save_image(form.image.data)
      current_user.image = picture_file
      db.session.commit()
      flash('Profile Image Updated Successfully!', 'success')
    return redirect (url_for('profile'))
   else:
    image = url_for('static', filename='user_uploads/' + str(current_user.image))
    return render_template('/avarter.html', title='Profile', image = image, form = form)

@app.route('/editprofile', methods=['GET', 'POST'])
@login_required
def editpro():

  # worker = Workers.query.get(email= current_user.email)
  worker = Workers.query.filter_by(email=current_user.email).first()
  form = EditBioForm()
  if form.validate_on_submit():
    worker.email= current_user.email
    worker.about= form.about.data
    worker.marrital_status= form.marrital_status.data
    worker.children= form.children.data
    worker.languages= form.languages.data
    worker.location = form.location.data
    worker.hobbies = form.hobbies.data
    worker.religion = form.religion.data
    worker.education = form.education.data
    db.session.commit()
    flash('Profile Updated Successfully!', 'success')
    return redirect (url_for('editpro'))
  elif request.method == 'GET':
    form.about.data = worker.about
    form.marrital_status.data = worker.marrital_status
    form.children.data = worker.children
    form.languages.data = worker.languages
    form.location.data = worker.location
    form.hobbies.data = worker.hobbies
    form.religion.data = worker.religion
    form.education.data = worker.education
  image = url_for('static', filename='user_uploads/' + str(current_user.image))
  return render_template('/editprofile.html', title='Profile', image = image, form = form)

  # this is a function to upload the user ID Card
def save_id_card(id_card):
  random_hex = secrets.token_hex(8)
  _, f_ext = os.path.splitext(id_card.filename)
  picture_fn = random_hex + f_ext
  picture_path = os.path.join(app.root_path, 'static/user_uploads', picture_fn)
  id_card.save(picture_path)
  return picture_fn
  
# this is a function to upload the user Prfile Picture 
def save_image(image):
  random_hex = secrets.token_hex(8)
  _, f_ext = os.path.splitext(image.filename)
  picture_fn = random_hex + f_ext
  picture_path = os.path.join(app.root_path, 'static/user_uploads', picture_fn)
  image.save(picture_path)
  return picture_fn


@app.route('/userprofile', methods=['GET', 'POST'])
@login_required
def profile():
  if current_user.role == 'User':
    form = UserCompleteRegForm()
    if form.validate_on_submit(): 
      if form.id_card.data:
        picture_file = save_id_card(form.id_card.data)
        current_user.address = form.address.data
        current_user.id_card = picture_file
        db.session.commit()
        flash('Your Registration is completed!', 'success')
      return redirect (url_for('home'))
    else:
      image = url_for('static', filename='user_uploads/' + str(current_user.image))
      return render_template('/userprofile.html', title='Profile', image = image, form = form)
  else:
    if current_user.pro_status == '1':

      form = EditBioForm()
      image = url_for('static', filename='user_uploads/' + str(current_user.image))
      return render_template('/editprofile.html', title='EditProfile', image = image, form = form)
    else:
     form = BioForm()
  if form.validate_on_submit(): 
    if form.id_card.data: 
      picture_file = save_image(form.image.data)
      current_user.image = picture_file
      picture_fill = save_id_card(form.id_card.data)
      current_user.id_card = picture_fill
      current_user.pro_status = 1
      worke = Workers(name=current_user.name, email=current_user.email, phone= current_user.phone, gender=current_user.gender, role = current_user.role, date_of_birth=current_user.date_of_birth, state_of_origin= current_user.state_of_origin, address=current_user.address, about= form.about.data, marrital_status=form.marrital_status.data, children = form.children.data, education=form.education.data, religion= form.religion.data, languages=form.languages.data,  location=form.location.data, hobbies = form.hobbies.data, worker_id = random.randint(0,999), number_of_jobs= 0, stars= 3, status= 1, id_card= picture_fill, image = picture_file, terms=1 )
      db.session.add(worke)
      db.session.commit()
      flash('Your Bio is completed! Please proceed with Guarrantors Registration', 'success')
    return redirect (url_for('grantt'))
  else:
    image = url_for('static', filename='user_uploads/' + str(current_user.image))
    return render_template('/userprofile.html', title='Profile', image = image, form = form)



@app.route('/guarrantor', methods=['GET', 'POST'])
@login_required
def grantt():
    form = GuarrantorForm()
    if form.validate_on_submit():
      email_exist = Guarrantor.query.filter_by(worker_email=current_user.email).first()
      if email_exist:
        flash(f'Sorry changes cannot be made, awaiting admin Verification. contact admin at admin@mama.com', 'success')
        image = url_for('static', filename='user_uploads/' + str(current_user.image)) 
        return render_template('/guarrantor.html',title='Guarrantor', image=image, form=form)
      else:
        picture_gua1 = save_id_card(form.guarrantor_one_id_card.data)
        picture_gua2 = save_id_card(form.guarrantor_two_id_card.data)
        user = Guarrantor(worker_email= current_user.email, guarrantor_one_name=form.guarrantor_one_name.data,guarrantor_two_name=form.guarrantor_two_name.data, guarrantor_one_phone=form.guarrantor_one_phone.data, guarrantor_two_phone=form.guarrantor_two_phone.data, guarrantor_one_address=form.guarrantor_one_address.data,  guarrantor_two_address=form.guarrantor_two_address.data, status=1, guarrantor_one_id_card =picture_gua1,guarrantor_two_id_card =picture_gua2)
        db.session.add(user)
        db.session.commit()
        flash(f'Guarrantor infor added Successfully !', 'success')
        return redirect (url_for('payme'))
    image = url_for('static', filename='user_uploads/' + str(current_user.image)) 
    return render_template('/guarrantor.html',title='Guarrantor', image=image, form=form)



@app.route('/Payment', methods=['GET', 'POST'])
@login_required
def payme():
  form = PaymentForm()
  if form.validate_on_submit():
      email_exist = Payment.query.filter_by(worker_email=current_user.email).first()
      if email_exist:
        flash(f'Sorry changes cannot be made, awaiting admin Verification. contact admin at admin@mama.com', 'success')
        image = url_for('static', filename='user_uploads/' + str(current_user.image)) 
        return render_template('/guarrantor.html',title='Guarrantor', image=image, form=form)
      else:
       
        user = Payment(worker_email= current_user.email, bank_name=form.bank_name.data,bank_account_number=form.bank_account_number.data, bank_account_name=form.bank_account_name.data, status=1)
        db.session.add(user)
        db.session.commit()
        flash(f'Payment infor added Successfully!', 'success')
        return redirect (url_for('acco'))
  image = url_for('static', filename='user_uploads/' + str(current_user.image))
  return render_template('/payment.html',title='Payment', image=image, form=form)



#This is the route to login to the system
@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      login_user(user)
      next_page = request.args.get('next')
      return redirect (next_page) if next_page else redirect (url_for('home'))
    else:
         flash(f'Incorrect or wrong Email / Password Combination! ', 'danger')
  return render_template('/login.html',title='Login', form=form)



@app.route('/user-signup', methods=['GET', 'POST'])
def usignup(): 
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = UserRegistrationForm()
  if form.validate_on_submit():
     hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
     user = User(name=form.name.data, email=form.email.data, password=hashed_password, phone= form.phone.data, gender=form.gender.data, terms=form.terms.data, role = 'User')
     db.session.add(user)
     db.session.commit()
     # flash(f'Account Created for {form.name.data} Successfully !', 'success')
     login_user(user)
     return redirect (url_for('home'))
     
  return render_template('user-signup.html' , title='User-Signup', form=form)

    
@app.route('/caregiver-signup', methods=['GET', 'POST'])
def wsignup():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = CaregiverRegistrationForm()
  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = User(name=form.name.data, email=form.email.data, password=hashed_password, phone= form.phone.data, gender=form.gender.data, terms=form.terms.data, role = form.role.data, date_of_birth=form.date_of_birth.data, state_of_origin= form.state_of_origin.data, address=form.address.data)
    db.session.add(user)
    db.session.commit()
    # flash(f'Account Created for {form.name.data} Successfully !', 'success')
    login_user(user)
    return redirect (url_for('home'))

  return render_template('caregiver-signup.html',title='Caregiver-Signup', form=form )


def send_reset_email(user):
  token = user.get_reset_token()
  msg = Message('Password Reset Request', sender='cellulantharry@gmail.com', recipients=[user.email])
  msg.body = f''' To reset your password visit the following link:
{url_for('reset_token', token= token, _external=True)}

If you did not make this request, kindly ignore this email and no changes will be made.

'''


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():

  # if current_user.is_authenticated:

    # return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit(): 
      user = User.query.filter_by(email = form.email.data).first()
      send_reset_email(user)
      flash(f'Email has been sent to {form.email.data} with instruction to reset your password', 'info')
      return redirect (url_for('login'))
    return render_template('/reset_request.html',  title='Reset Password', form=form)
   

@app.route('/reset_request/<token>', methods=['GET', 'POST'])
def reset_token(token):

  if current_user.is_authenticated:
    return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
      flash(f'Sorry your token is Invalid or Expired !', 'warning')
      return redirect (url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
      hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
      user.password = hashed_password
      db.session.commit()
      flash(f'Your Password has been updated successfully. you are now able to login.', 'success')
      return redirect ('login')

    return render_template('/reset_token.html',title='Reset Password', form=form) 
      


@app.route('/logout', methods=['GET', 'POST'])
def logout():
  logout_user()
  return redirect(url_for('index'))
   