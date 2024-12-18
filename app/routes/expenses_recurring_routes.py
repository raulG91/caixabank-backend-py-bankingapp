from . import expenses_bp
from flask import request,jsonify,Response
from app.models import ExpenseRecurring,User
from flask_jwt_extended import JWTManager,jwt_required,get_jwt_identity
from app.utils.functions import check_mandatory_fields,add_months
import json
from datetime import datetime,timedelta
from calendar import monthrange



@expenses_bp.route('/',methods=['POST'])
@jwt_required()
def new_expense():
    user_email = get_jwt_identity()
    user = User.user_exist(user_email)
    expense_info = request.get_json()
    if user:
        # Check if all mandatory fields are in the incoming payload
        if check_mandatory_fields(['expense_name','amount','frequency','start_date'],expense_info):
            #check if fields are not empty
            if (expense_info['expense_name']!= "" and expense_info['expense_name']!= None) and (expense_info['amount'] !="" and expense_info['amount']!= None) and (expense_info['frequency'] !="" and expense_info['frequency']!= None) and (expense_info['start_date'] !="" and expense_info['start_date']!= None):
                new_expense = ExpenseRecurring(expense_name=expense_info['expense_name'],amount=expense_info['amount'],frequency=expense_info['frequency'],start_date=expense_info['start_date'],user_id=user.getId())
                if new_expense.save():
                    print(type(new_expense.getStartDate()))
                    return jsonify({
                        "msg":"Recurring expense added successfully",
                        "data":{
                            "id":new_expense.getId(),
                            "expense_name": new_expense.getName(),
                            "amount": new_expense.getAmount(),
                            "frequency": new_expense.getFrequency(),
                            "start_date": new_expense.getStartDate().strftime("%Y-%m-%d")
                        }
                    }),201
                else:
                    return Response(response=json.dumps({"msg":"Internal error"}),status=500,mimetype='application/json')
            else:
                return Response(response=json.dumps({"msg":"No empty fields allowed"}),status=400,mimetype="application/json")
        else:
            return Response(response=json.dumps({"msg":"No data provided."}),status=400,mimetype='application/json')

    else:
        return Response(status=401)

@expenses_bp.route('/',methods=['GET'])
@jwt_required()
def get_expenses():
    user_email = get_jwt_identity()
    #Get user data
    user:User = User.user_exist(user_email)
    user_expenses:list[ExpenseRecurring] = ExpenseRecurring.query.filter_by(user_id = user.getId()).all()

    return jsonify([expense.toJSON() for expense in user_expenses])

@expenses_bp.route('/<int:expense_id>',methods=['PUT'])
@jwt_required()
def update_expense(expense_id):
    user_email = get_jwt_identity()
    user:User = User.user_exist(user_email)
    expense_info = request.get_json()

    if check_mandatory_fields(['expense_name','amount','frequency','start_date'],expense_info):
        #Check if fields are populated
        if (expense_info['expense_name']!= "" and expense_info['expense_name']!= None) and (expense_info['amount'] !="" and expense_info['amount']!= None) and (expense_info['frequency'] !="" and expense_info['frequency']!= None) and (expense_info['start_date'] !="" and expense_info['start_date']!= None):
            #Check if the expense exist and is associated to the user
            expense:ExpenseRecurring = ExpenseRecurring.query.filter_by(id=expense_id,user_id = user.getId()).first()
            if expense:
                #Update expense in the database
                expense.setName(expense_info['expense_name'])
                expense.setAmount(expense_info['amount'])
                expense.setFrequency(expense_info['frequency'])
                expense.setStartDate(expense_info['start_date'])
                if expense.save():
                    return jsonify({
                        "msg":"Recurring expense updated successfully",
                        "data":{
                            "id":expense.getId(),
                            "expense_name": expense.getName(),
                            "amount": expense.getAmount(),
                            "frequency": expense.getFrequency(),
                            "start_date": expense.getStartDate()
                        }
                    })
                else:
                    #Error updating expense
                     return Response(response=json.dumps({"msg":"Internal error"}),status=500,mimetype='application/json')
            else:
                #Expense doesn't exist
                return Response(response=json.dumps({"msg":"Expense not found."}),status=404,mimetype='application/json')
        else:
            return Response(response=json.dumps({"msg":"No empty fields allowed."}),status=400,mimetype='application/json')
    else:
        return Response(response=json.dumps({"msg":"No data provided."}),status=400,mimetype='application/json')

@expenses_bp.route('/<int:expense_id>',methods=['DELETE'])
@jwt_required()
def delete_expense(expense_id):
    user_email = get_jwt_identity()
    user:User = User.user_exist(user_email)
    #Check if the expense exist in the system for the logged user

    expense:ExpenseRecurring=ExpenseRecurring.query.filter_by(id=expense_id,user_id=user.getId()).first()

    if expense:
        if expense.delete_expense():
            return Response(response=json.dumps({"msg":"Recurring expense deleted successfully."}),status=404,mimetype='application/json')

    else:
        return Response(response=json.dumps({"msg":"Expense not found."}),status=404,mimetype='application/json')


@expenses_bp.route('/projection',methods=['GET'])
@jwt_required()
def projection():
    user_email = get_jwt_identity()
    user:User = User.user_exist(user_email)
    today = datetime.today()
    #Count one year for first day of current month
    one_year =datetime(today.year,today.month,1) + timedelta(days=365)
    #Find all expenses for the user withn 12 months
    try:
        expenses = ExpenseRecurring.query.filter(
            ExpenseRecurring.user_id == user.getId(),
            ExpenseRecurring.start_date <= one_year     
            ).all()
    except:
        return Response(response="Internal error",status=500,mimetype='plain/text')
    if len(expenses) > 0:
        projection_list=[]
        reference_date = today
        for _ in range(12):
            #Iterate over the year and calculate balance.
            total = 0.0
            first_month_day = reference_date.replace(day=1)
            #Get last date of the month
            last_month_day = reference_date.replace(day=monthrange(reference_date.year, reference_date.month)[1])

            for expense in expenses:
                if expense.getStartDate() <= last_month_day:
                    total += expense.getAmount()
            projection_list.append({
                "month": f'{reference_date.strftime("%Y-%m")}',
                "recurring_expenses": round(total,2)
            })
            # Move to the next month
            if reference_date.month == 12:
                reference_date = reference_date.replace(year=reference_date.year + 1, month=1)
            else:
                reference_date = reference_date.replace(month=reference_date.month + 1)
        return jsonify(projection_list)
    else:
        return jsonify([])
        
