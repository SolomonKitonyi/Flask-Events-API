from flask import Blueprint 
from flask_restful import Api,Resource, reqparse 
from models import User, db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import  create_access_token, JWTManager



auth_bp = Blueprint('auth_bp',__name__, url_prefix='/auth')
bcrypt = Bcrypt()
jwt = JWTManager()
auth_api = Api(auth_bp)
# auth 

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).first()


register_args = reqparse.RequestParser()
register_args.add_argument('email')
register_args.add_argument('password')
register_args.add_argument('username')


login_args = reqparse.RequestParser()
login_args.add_argument('email')
login_args.add_argument('password')

class Register(Resource):
     

     def post(self):

        data = register_args.parse_args()
        hashed_password = bcrypt.generate_password_hash(data.get('password'))
        new_user = User(email = data.get('email'), username = data.get('username'),password= hashed_password )
        db.session.add(new_user)
        db.session.commit()

        return {"msg":'user created successfully'}
     

class Login(Resource):

    def post(self):
        data = login_args.parse_args()
        # check if the user exists in our db 
        user = User.query.filter_by(email=data.get('email')).first()
        if not user:
            return {"msg":"User Does not exists in our DB"}
        if not bcrypt.check_password_hash(user.password, data.get('password')):
            return {"msg": "Password is incorrect!"}
        # check if the password is correct 
        
        # login
        token = create_access_token(identity=user.id)
        return {"token":token}


          
          




# routes
auth_api.add_resource(Register,'/register')
auth_api.add_resource(Login,'/login')
