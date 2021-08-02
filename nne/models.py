from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from nne import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
  return User.query.filter_by(id=user_id).first()   


class User(db.Model, UserMixin):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), unique=True, nullable=False)
    role = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(255), nullable=False)
    terms = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    date_of_birth =db.Column(db.String(255), nullable=True)
    state_of_origin = db.Column(db.String(255), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    image = db.Column(db.String(255), nullable=True, default='default.jpg')
    id_card = db.Column(db.String(255), nullable=True)
    pro_status = db.Column(db.String(255), nullable=True, default= 0)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
        
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    
class Users(db.Model, UserMixin):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), unique=True, nullable=False)
    role = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime())
    terms = db.Column(db.String(255), nullable=False)
    date_of_birth =db.Column(db.String(255), nullable=True)
    state_of_origin = db.Column(db.String(255), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    image = db.Column(db.String(255), nullable=True, default='default.jpg')
    id_card = db.Column(db.String(255), nullable=True)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())

class Workers(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    worker_id = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(255), unique=True, nullable=False)
    role = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(255), nullable=False)
    terms = db.Column(db.String(255), nullable=True)
    date_of_birth =db.Column(db.String(255), nullable=True)
    state_of_origin = db.Column(db.String(255), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    about = db.Column(db.String(255), nullable=True)
    id_card = db.Column(db.String(255), nullable=True)
    marrital_status = db.Column(db.String(255), nullable=True)
    children = db.Column(db.String(255), nullable=True)
    education = db.Column(db.String(255), nullable=True)
    religion = db.Column(db.String(255), nullable=True)
    languages = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(255), nullable=True)
    hobbies = db.Column(db.String(255), nullable=True)
    number_of_jobs = db.Column(db.String(255), nullable=True)
    stars = db.Column(db.String(255), nullable=True)
    image = db.Column(db.String(255), nullable=True, default='default.jpg')
    completed_at = db.Column(db.DateTime(), default=datetime.utcnow)
    status = db.Column(db.String(255), nullable=True, default= 0)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())  

       
class Guarrantor(db.Model, UserMixin):
    
    id = db.Column(db.Integer, primary_key=True)
    worker_email = db.Column(db.String(255), unique=True, nullable=False)
    guarrantor_one_name = db.Column(db.String(255), nullable=False)
    guarrantor_two_name = db.Column(db.String(255), nullable=False)
    guarrantor_one_phone = db.Column(db.String(255), nullable=False)
    guarrantor_two_phone = db.Column(db.String(255), nullable=False)
    guarrantor_one_address = db.Column(db.String(255), nullable=False)
    guarrantor_two_address = db.Column(db.String(255), nullable=False)
    guarrantor_one_id_card = db.Column(db.String(255), nullable=False)
    guarrantor_two_id_card = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(255), nullable=True, default= 0)
    completed_at = db.Column(db.DateTime(), default=datetime.utcnow)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
 

class Payment(db.Model, UserMixin):
    
    id = db.Column(db.Integer, primary_key=True)
    worker_email = db.Column(db.String(255), unique=True, nullable=False)
    bank_name = db.Column(db.String(255), nullable=False)
    bank_account_number = db.Column(db.String(255), nullable=False)
    bank_account_name = db. Column(db.String(255), nullable=False)
    status = db.Column(db.String(255), nullable=True, default= 0)
    completed_at = db.Column(db.DateTime(), default=datetime.utcnow)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())