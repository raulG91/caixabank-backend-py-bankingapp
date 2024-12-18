from . import user_bp
from flask import request,jsonify,Response,current_app
from app.utils.functions import check_email
from app.models import User
from flask_jwt_extended import JWTManager, create_access_token
import hmac
import hashlib

@user_bp.route('/register',methods=['POST'])
def register_user():
    user_info = request.get_json()
    mandatory_fields = set(['email','name','password'])
    if mandatory_fields.issubset(user_info.keys()):
        if (user_info['name'] != "" and user_info['name'] != None) and (user_info['email'] != "" and user_info['email'] != None) and (user_info['password'] !="" and user_info['password'] != None):
           #Check inbound data types
            if isinstance(user_info['name'],str) and isinstance(user_info['password'],str) and isinstance(user_info['email'],str) :
                 #Check if email is correct
                if check_email(user_info['email']):
                    if not User.user_exist(user_info['email']):
                        new_user = User(user_info['email'],user_info['password'],user_info['name'])
                        if new_user.save():
                            return jsonify({"name":new_user.getName(),"hashedPassword":mask_hash(new_user.getPassword()),"email":new_user.getEmail()}),201
                        else:
                            return Response(response="Internal server error",status=500, mimetype='text/plain')
                    else:
                        return Response(response="Email already exists",status=400,mimetype='text/plain')
                else:
                    return Response(status=400,response=f'Invalid email: {user_info['email']}',mimetype='text/plain')
            else:
                return Response(status=400,response='Invalid input types',mimetype='text/plain')

        else:
            #There empty fields in the request return error 400
            return Response(status=400,response="No empty fields are allowed",mimetype='text/plain')
    else:
        #Missing fileds in the request
        return  Response(status=400,response='All fields are required.',mimetype='text/plain')
    
@user_bp.route('/login',methods=['POST'])
def login():
    login_info = request.get_json()
    mandatory_fields = set(['email','password'])
    if mandatory_fields.issubset(login_info.keys()):
        #First check if all fields are populated
        if (login_info['email'] != "" and login_info['email'] != None) and (login_info['password'] != "" and login_info['password'] != None):
            if isinstance(login_info['email'],str) and isinstance(login_info['password'],str):
                #Second check, user must exist in the database
                user:User = User.user_exist(login_info['email'])
                if user:
                    #Third, check if passwords match
                    if user.checkPassword(login_info['password']):
                        #Create JWT token
                        token = create_access_token(identity=user.getEmail())
                        return jsonify({"token":token})
                    else:
                        # Password doesn't match with the hash in the database
                        return Response(response="Bad credentials",status=401,mimetype='text/plain')    

                else:
                    #User not found in the database
                    return Response(response=f'User not found for the given email: {login_info['email']}',status=400,mimetype='text/plain')
            else:
                #Any of the fields are not type string
                return Response(response="Invalid input types",status=400,mimetype='text/plain')        
        else:
            return Response(response="Bad credentials",status=401,mimetype="text/plain")
    else:
        #Retrun error since not information is in the payload
        return Response(response="All fields are required", status = 401, mimetype="text/plain")


# Mask the hash with HMAC
def mask_hash(password_hash):
    print(type(current_app.config.get('SECRET_KEY')))
    return hmac.new(current_app.config.get('SECRET_KEY').encode(), password_hash.encode(), hashlib.sha256).hexdigest()