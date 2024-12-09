from . import alerts_bp
from flask import request,jsonify,Response
from app.models import User,Alerts
from flask_jwt_extended import JWTManager,jwt_required,get_jwt_identity
from app.utils.functions import check_mandatory_fields
import json


@alerts_bp.route('/amount_reached',methods=['POST'])
@jwt_required()
def amount_reached():

    user_email = get_jwt_identity()
    user:User = User.user_exist(user_email)
    alert_info = request.get_json()

    if user:
        if check_mandatory_fields(['target_amount','alert_threshold'],alert_info):
            if (alert_info['target_amount'] != "" and alert_info['target_amount'] != None) and (alert_info['alert_threshold'] != "" and alert_info['alert_threshold'] != None):
                alert = Alerts(float(alert_info['target_amount']),float(alert_info['alert_threshold']),0,user.getId())
                if alert.save():
                    return Response(json.dumps({
                        "msg":"Correctly added savings alert!",
                        "data":{
                            "id":alert.getId(),
                            "user_id":user.getId(),
                            "target_amount": alert.get_target_amount(),
                            "alert_threshold": alert.get_alert_threshold()
                        }
                    }),status=201,mimetype='application/json')
                else:
                    return Response(response=json.dumps({"msg":"Internal error"}),status=500,mimetype='application/json')

            else:
                return Response(response=json.dumps({"msg":"No empty fields allowed."}),status=400,mimetype='application/json')
        else:
            return Response(response=json.dumps({"msg":"No empty fields allowed."}),status=400,mimetype='application/json')
    else:
        return Response(status=401)

@alerts_bp.route('/balance_drop',methods=['POST'])
@jwt_required()
def balance_drop():
    user_email = get_jwt_identity()
    user:User = User.user_exist(user_email)
    balance_info = request.get_json()
    if user:
        #Check if all mandatory fields are in the request
        if check_mandatory_fields(['balance_drop_threshold'],balance_info):
            #Check if payload is not empty
            if balance_info['balance_drop_threshold'] != None and balance_info['balance_drop_threshold'] != "":
                alert = Alerts(0,0,float(balance_info['balance_drop_threshold']),user.getId())
                #Save the alert in the database
                if alert.save():
                    return Response(response=json.dumps({
                        "msg":"Correctly added balance drop alert!",
                        "data":{
                            "id": alert.getId(),
                            "user_id":user.getId(),
                            "balance_drop_threshold":alert.get_balance_threshold()
                        }
                    }),status=201,mimetype='application/json')
                else:
                    return Response(response=json.dumps({"msg":"Internal error"}),status=500,mimetype='application/json')
                
            else:
                return Response(response=json.dumps({"msg":"No empty fields allowed."}),status=400,mimetype='application/json')
        else:
            return Response(response=json.dumps({"msg":"No empty fields allowed."}),status=400,mimetype='application/json')
           
    else:
        return Response(status=401)

@alerts_bp.route('/delete',methods=['POST'])
@jwt_required()
def delete_alert():
    user_email = get_jwt_identity()
    user:User = User.user_exist(user_email)
    #Get inbound payload
    alert_info = request.get_json()

    if check_mandatory_fields(['alert_id'],alert_info):
        if alert_info['alert_id'] != None and alert_info['alert_id'] != "" and isinstance(alert_info['alert_id'],int):
            #Find introduced alert in the database 
            alert = Alerts.query.filter_by(id=alert_info['alert_id'],user_id = user.getId()).first()

            if alert:
                #Alert has been found in the database
                if alert.delete():
                    return Response(response=json.dumps({"msg":"Alert deleted successfully."}),status=200,mimetype='application/json')
                else:
                    # Error deleting alert
                    return Response(response=json.dumps({"msg":"Internal error."}),status=500,mimetype='application/json')
            else:
                #Alert not found or not link to user
                return Response(response=json.dumps({"msg":"Alert not found."}),status=404,mimetype='application/json')
        else:
            # Missing alert_id
            return Response(response=json.dumps({"msg":"Missing alert ID."}),status=400,mimetype='application/json')
    else:
        return Response(response=json.dumps({"msg":"No empty fields allowed."}),status=400,mimetype='application/json')

@alerts_bp.route('/list',methods=['GET'])
@jwt_required()
def list_alerts():
    user_email = get_jwt_identity()
    user:User = User.user_exist(user_email)

    if user:
        #Get all alerts from the database
        alert_list = Alerts.query.filter_by(user_id = user.getId()).all()
        final_array = []
        if len(alert_list) > 0:
            for alert in alert_list:
                final_array.append({
                    "id": alert.getId(),
                    "user_id": user.getId(),
                    "target_amount": alert.get_target_amount(),
                    "alert_threshold": alert.get_alert_threshold(),
                    "balance_drop_threshold": alert.get_balance_threshold()
                })
            #Build final response
            return Response(response=json.dumps({"data":final_array}),status=200,mimetype='application/json')    
            
        else:
            return jsonify({"data":[]}),200

    else:
        return Response(response=json.dumps({"msg":"User doesn't exist"}),status=401,mimetype='application/json')