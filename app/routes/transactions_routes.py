from . import transaction_bp
from flask import request,jsonify,Response,current_app
from app.models import User,Transaction,Alerts
from flask_jwt_extended import JWTManager,jwt_required,get_jwt_identity
from app.utils.functions import check_mandatory_fields
from datetime import datetime,timezone,timedelta
import json
import numpy as np
from dateutil.relativedelta import relativedelta
from flask_mail import Message,Mail
import logging
import smtplib
import smtplib
from email.mime.text import MIMEText
from email.message import EmailMessage

@transaction_bp.route('/transactions',methods=['POST'])
@jwt_required()
def new_transaction():
    user_email = get_jwt_identity()
    user:User = User.user_exist(user_email)
    transaction_info = request.get_json()
    if user :
        if check_mandatory_fields(['user_id','amount','category'],transaction_info):
            if (transaction_info['user_id'] != "" and transaction_info['user_id'] != None) and (transaction_info['amount'] != "" and transaction_info['amount'] != None) and (transaction_info['category'] != "" and transaction_info['category'] != None):
                if isinstance(transaction_info['user_id'],int) and isinstance(transaction_info['amount'],float) and isinstance(transaction_info['category'],str):
                    if 'timestamp' in transaction_info:
                        transaction = Transaction(user.getId(),transaction_info['amount'],transaction_info['category'],transaction_info['timestamp'])
                    else:
                        transaction = Transaction(user.getId(),transaction_info['amount'],transaction_info['category'])

                    transaction.setFraud(check_fraud(transaction))
                    if transaction.save():
                        #Transaction was saved in the database
                        #Now update user balance
                        user.setBalance(user.getBalance()-transaction.getAmount())
                        if user.save():
                            alerts(transaction,user)
                            return Response(response=json.dumps({
                                "msg": "Transaction added and evaluated for fraud.",
                                "data":{
                                    "id": transaction.getId(),
                                    "user_id": user.getId(),
                                    "amount": transaction.getAmount(),
                                    "category": transaction.getCategory(),
                                    "timestamp": transaction.getTimestamp(),
                                    "fraud": transaction.getFraud()
                                }
                            }),status=201,mimetype='application/json')
                        else:
                            return Response(response=json.dumps({"msg":"Internal error"}),status=500,mimetype='application/json')
                    else:
                        return Response(response=json.dumps({"msg":"Internal error"}),status=500,mimetype='application/json')
                else:
                    return Response(response=json.dumps({"msg":"Invalid input types"}),status=400,mimetype='application/json')
            else:
                 return Response(response=json.dumps({"msg":"No empty fields allowed."}),status=400,mimetype='application/json')
               
        else:
            return Response(response=json.dumps({"msg":"No data provided."}),status=400,mimetype='application/json')
       
    else:
        return Response(response=json.dumps({"msg":"User doesn't exist"}),status=401,mimetype='application/json')
    
def check_fraud(transaction:Transaction):

    #First check: if the amount exceeds 3 standard deviations from the customer's average daily spending 
    # over the 90 days prior to the transaction.
    is_fraud = False

    reference_date = transaction.getTimestampDBFormat()
  
    start_date = reference_date - timedelta(days=90)
    try:
        #Get all transactions in the previous 90 days
        previous_transactions = Transaction.query.filter(
            Transaction.user_id == transaction.getUserId(),
            Transaction.timestamp <= reference_date,
            Transaction.timestamp >= start_date
        ).all()
    except Exception as e:
        print(e)

    day_totals = {}
    #Calculate total amount for each day
    for trans in previous_transactions:
        day = trans.getTimestampDBFormat().date()
        day_totals[day] = day_totals.get(day,0) + trans.getAmount()

    #List with all amounts
    daily_amount = list(day_totals.values())
    if len(daily_amount) >= 2:
        #calculate averrage and standard for daily amouts
        averrage= np.average(daily_amount)
        standard_desviation = np.std(daily_amount)
        threshold = averrage + (3 * standard_desviation)
        is_fraud = transaction.getAmount() > threshold

    if is_fraud:
        return is_fraud

    #Second check: Marks as fraud if it is category didn't use in the last six months

    start_date = reference_date - relativedelta(months=6)
    try:
        #Get all transactions in the previous 6 months
        previous_transactions = Transaction.query.filter(
            Transaction.user_id == transaction.getUserId(),
            Transaction.timestamp <= reference_date,
            Transaction.timestamp >= start_date
        ).all()
    except Exception as e:
        print(e)

    categories = [x.getCategory() for x in previous_transactions]

    is_fraud = not (transaction.getCategory() in categories)
    
    if is_fraud:
        return is_fraud

    #Third check: More than 3 transactions occurs in the las 5 minutes and the combined cost exceed daily sverrage spend

    #Check if there are 3 trasactions in the last 5 minutes
    start_date = reference_date - timedelta(minutes=5)

    try:
        #Get all transactions in the previous 5 minutes
        previous_transactions = Transaction.query.filter(
            Transaction.user_id == transaction.getUserId(),
            Transaction.timestamp <= reference_date,
            Transaction.timestamp >= start_date
        ).all()
    except Exception as e:
        print(e)

    if(len(previous_transactions) >= 3):
        #Compute amounts for those transactions
        sum_amounts = 0
        for trans in previous_transactions:
            sum_amounts += trans.getAmount()
            

        # Now check daily averrage spend
        try:
            user_transactions = Transaction.query.filter_by(user_id = transaction.getUserId()).all()
            day_totals = {}
            for trans in user_transactions:
                day = trans.getTimestampDBFormat().date()
                day_totals[day] = day_totals.get(day,0) + trans.getAmount()
            daily_amount = list(day_totals.values())
            averrage_spend = np.average(daily_amount)
            is_fraud = sum_amounts > averrage_spend
        except Exception as e:
            print(e)          
     
    return is_fraud
def send_email_alert(email,subject,body):
    logging.basicConfig(level=logging.DEBUG)
    smtplib.SMTP.debuglevel = 1  # Enable debug messages for SMTP
    try:
        with smtplib.SMTP(current_app.config.get('MAIL_SERVER'), 1025) as server:
            server.ehlo()  # Send EHLO command
            email_message = EmailMessage()
            email_message["From"] = current_app.config.get('MAIL_DEFAULT_SENDER')
            email_message["To"] = email
            email_message["Subject"] = subject
            email_message.set_content(body)
            # Send the email
            server.sendmail(current_app.config.get('MAIL_DEFAULT_SENDER'), email, email_message.as_string())
            print(f"Email sent successfully")
    except Exception as e:
        print(f"Error: {e}")


def alerts(transaction:Transaction,user:User):
    
    #Check if the balance has dropped under the limit

    #Find if the user has any alert
    try:
        alerts = Alerts.query.filter(
            Alerts.user_id == user.getId()
        ).all()
    except Exception as e:
        print(e)


    for alert in alerts:
        if (alert.get_balance_threshold() != None) and (alert.get_balance_threshold() > 0) and (user.getBalance() <= alert.get_balance_threshold()):
            email_body = f'Dear {user.getName()},\n\nWe noticed a significant balance drop in your account more than \n{alert.get_balance_threshold()}.\nIf this wasn\'t you, please review your recent transactions to ensure \neverything is correct.\n\nBest Regards,\nThe Management Team'
            send_email_alert(user.getEmail(),"Balance drop alert",email_body)
        elif(alert.get_alert_threshold() != None) and (alert.get_alert_threshold() > 0) and (user.getBalance()>= alert.get_alert_threshold()):
            email_body =  f'Dear {user.getName()},\n\nGreat news! Your savings are nearing the target amount of \n{alert.get_target_amount()}\nKeep up the great work and stay consistent!\n\nBest Regards,\nThe Management Team'    
            send_email_alert(user.getEmail(),"Saving alert",email_body)
       