from . import transfers_bp
from flask import request,jsonify,Response
from app.models import ExpenseRecurring,User
from flask_jwt_extended import JWTManager,jwt_required,get_jwt_identity
from app.utils.functions import check_mandatory_fields
import json
import csv
import os

@transfers_bp.route('/simulate',methods=['GET'])
@jwt_required()
def simulate():
    
    transfer_info = request.get_json()
    
    if check_mandatory_fields(['amount','source_currency','target_currency'],transfer_info):
        if (transfer_info['amount'] != "" and transfer_info['amount']!= None) and (transfer_info['source_currency'] != "" and transfer_info['source_currency']!= None) and (transfer_info['target_currency'] != "" and transfer_info['target_currency']!= None):
            #Read exchange rates
            rates_path = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,'exchange_rates.csv'))
            fees_path = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,'exchange_fees.csv'))
            try:
                #Read conversion rates
                with open(rates_path,newline='') as csvfile:
                    spamreader=csv.reader(csvfile,delimiter=',')
                    conversion_rates = []
                    for row in spamreader:
                       conversion_rates.append(row)
                #Read exchange fees 
                with open(fees_path,newline='') as csvfile:
                    spamreader=csv.reader(csvfile,delimiter=',')
                    conversion_fees=[]
                    for row in spamreader:
                        conversion_fees.append(row)
            except Exception as e:
                return Response(response=e,status=500,mimetype='plain/text')
            
            for row in conversion_rates:
                if row[0] == transfer_info['source_currency'] and row[1] == transfer_info['target_currency']:
                    rate = row[2]
                    for fee in conversion_fees:
                        if fee[0]==transfer_info['source_currency'] and fee[1] == transfer_info['target_currency']:
                            fee = fee[2]
                            target_amount = float(transfer_info['amount']) * (1-float(fee)) * float(rate)
                            return jsonify({"msg": f'Amount in target currency: {target_amount}.'}),201
            return Response(json.dumps({"msg":"Invalid currencies or no exchange data available."}),status=404,mimetype='application/json')   
        else:
            return Response(response=json.dumps({"msg":"No empty fields allowed."}),status=400,mimetype='application/json')
    else:
        return Response(response=json.dumps({"msg":"No empty fields allowed."}),status=400,mimetype='application/json')

@transfers_bp.route('/fees',methods=['GET'])
@jwt_required()
def get_fess():
    if 'source_currency' in request.args and 'target_currency' in request.args:
        #Check if the fields are not empty 
        if(request.args['source_currency']!="" and request.args['source_currency']!= None) and (request.args['target_currency']!="" and request.args['target_currency']!=None):
            #Read exchange fees
            source_currency = request.args['source_currency']
            target_currency = request.args['target_currency']
            fees_path = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,'exchange_fees.csv'))
            with open(fees_path,newline='') as csvfile:
                spamreader = csv.reader(csvfile,delimiter=',')
                for row in spamreader:
                    if row[0] == source_currency and row[1] == target_currency:
                        return jsonify({"fee":float(row[2])})
                    
                return Response(response=json.dumps({"msg":"No fee information available for these currencies."}),status=404,mimetype='application/json')    


        else:
            return Response(response=json.dumps({"msg":"No empty fields allowed."}),status=400,mimetype='application/json')

    else:
        return Response(response=json.dumps({"msg":"No empty fields allowed."}),status=400,mimetype='application/json')

@transfers_bp.route('/rates',methods=['GET'])
@jwt_required()
def get_rates():

    if 'source_currency' in request.args and 'target_currency' in request.args:
        #Read exchange rate
        source_currency = request.args['source_currency']
        target_currency = request.args['target_currency']
        rates_path = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,'exchange_rates.csv'))    
        try:
            with open(rates_path,newline='') as csvfile:
                spamreader = csv.reader(csvfile,delimiter=',')
                for row in spamreader:
                    if row[0] == source_currency and row[1] == target_currency:
                        #Rate is found
                        return jsonify({"rate":float(row[2])})
                #if change rate is not found
                return Response(response=json.dumps({"msg":"No exchange rate available for these currencies."}),status=404,mimetype='application/json')
        except Exception as e:
            return jsonify({"Error":"Error opening rates file"}),500       
    else:
        return Response(response=json.dumps({"msg":"No empty fields allowed."}),status=400,mimetype='application/json')
