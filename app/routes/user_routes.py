from . import user_bp
from flask import request,jsonify,Response
from app.utils.functions import check_email
from app.models import User
from flask_jwt_extended import JWTManager, create_access_token

@user_bp.route('/register',methods=['POST'])
def register_user():
    user_info = request.get_json()
    mandatory_fields = set(['email','name','password'])
    if mandatory_fields.issubset(user_info.keys()):
        if (user_info['name'] != "" and user_info['name'] != None) and (user_info['email'] != "" and user_info['email'] != None) and (user_info['password'] !="" and user_info['password'] != None):
            #Check if email is correct
            if check_email(user_info['email']):
                if not User.user_exist(user_info['email']):
                    new_user = User(user_info['email'],user_info['password'],user_info['name'])
                    if new_user.save():
                        return jsonify({"name":new_user.getName(),"hashedPassword":new_user.getPassword(),"email":new_user.getEmail()})
                    else:
                        return Response(response="Internal server error",status=500, mimetype='text/plain')
                else:
                    return Response(response="Email already exists",status=400,mimetype='text/plain')
            else:
                return Response(status=400,response=f'Invalid email: {user_info['email']}',mimetype='text/plain')
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
            #Second check, user must exist in the database
            user:User = User.user_exist(login_info['email'])
            if user:
                #Third, check if passwords match
                if user.checkPassword(login_info['password']):
                    #Create JWT toke
                    token = create_access_token(identity=user.getEmail())
                    return jsonify({"token":token})
                else:
                    return Response(response="Bad credentials",status=401,mimetype='text/plain')    

            else:
                return Response(response=f'User not found for the given email: {login_info['email']}',status=400,mimetype='text/plain')
        else:
            return Response(response="Bad credentials",status=400,mimetype="text/plain")
    else:
        #Retrun error since not information is in the payload
        return Response(response="All fields are required", status = 400, mimetype="text/plain")
