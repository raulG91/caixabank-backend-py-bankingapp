from werkzeug.security import generate_password_hash,check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timezone
import json
db = SQLAlchemy()
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(128),nullable=False)
    email = db.Column(db.String(128),nullable=False)
    hashed_password = db.Column(db.String(128),nullable=False)
    balance = db.Column(db.Float)

    def __init__(self,email,password,name):
        self.email = email
        self.name = name
        self.hashed_password = generate_password_hash(password=password,method='pbkdf2')
        self.balance = 0 
    def getName(self):
        return self.name
    def getPassword(self):
        return self.hashed_password
    def checkPassword(self,password):
        return check_password_hash(self.hashed_password,password)
    def getEmail(self)->str:
        return self.email
    def getId(self):
        return self.id
    def getBalance(self):
        return self.balance
    def setBalance(self,new_balance):
        self.balance = new_balance    
    def setName(self,name):
        self.name = name
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()    
            return self
        except Exception as e:
            print("Error guardando usuario" , e)
            return False
    @classmethod
    def user_exist(cls,email):
        user = cls.query.filter_by(email=email).first()
        if user is not None:
            return user
        else:
            return False    

class ExpenseRecurring(db.Model):
        __tablename__='recurring_expenses'
        id= db.Column(db.Integer,primary_key=True)
        user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
        expense_name = db.Column(db.String(255),nullable=False)
        amount = db.Column(db.Float,nullable=False)
        frequency = db.Column(db.String(50),nullable=False)
        start_date = db.Column(db.DateTime(),nullable=False)
        created_at = db.Column(db.DateTime(),nullable=False)
        def __init__(self,expense_name,amount,frequency,start_date,user_id):
            self.expense_name = expense_name
            self.user_id = user_id
            self.amount = amount
            self.frequency = frequency
            self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
            self.created_at = datetime.today()
        def getId(self):
            return self.id
        def getUser(self):
            return self.user_id
        def getName(self):
            return self.expense_name
        def setName(self,expense_name):
            self.expense_name = expense_name
        def getFrequency(self):
            return self.frequency
        def setFrequency(self,frequency):
            self.frequency = frequency
        def getStartDate(self):
            return self.start_date 
        def setStartDate(self,start_date):
            year,month,day = start_date.split("-")
            self.start_date = datetime(int(year),int(month),int(day))           
        def getAmount(self):
            return self.amount  
        def setAmount(self,amount):
            self.amount=amount
        def toJSON(self) -> dict:
            return {
                    "id":self.id,
                    "expense_name": self.expense_name,
                    "amount": self.amount,
                    "frequency": self.frequency,
                    "start_date": self.start_date.strftime("%Y-%m-%d"),
                    "created_at": self.created_at.strftime("%Y-%m-%d")
                }
            
        def save(self):
            try:
                db.session.add(self)
                db.session.commit()
                return self
            except Exception as e:
                return False   
        def delete_expense(self):
            try:
                db.session.delete(self)
                db.session.commit()    
                return self
            except Exception as e:
                return False      
            
class Alerts(db.Model):
    __tablename__= 'alerts'
    id=db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    target_amount=db.Column(db.Float)
    alert_threshold = db.Column(db.Float)
    balance_drop_threshold = db.Column(db.Float)
    created_at = db.Column(db.DateTime()) 

    def __init__(self,target_amout,alert_threshold,balance_drop,user_id):
        self.target_amount = target_amout
        self.alert_threshold = alert_threshold
        self.user_id = user_id
        self.balance_drop_threshold = balance_drop
        self.created_at = datetime.now()
    def getId(self)->int:
        return self.id
    def get_target_amount(self):
        return self.target_amount
    def get_alert_threshold(self):
        return self.alert_threshold
    def get_balance_threshold(self):
        return self.balance_drop_threshold
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except Exception as e:
            return False   
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()    
            return self
        except Exception as e:
            return False          

class Transaction(db.Model):
    __tablename__= "transactions"
    id=db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    amount = db.Column(db.Float)
    category = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime())
    fraud = db.Column(db.Boolean)

    def __init__(self,user_id,amount,category,timestamp=""):
        self.user_id = user_id
        self.amount= amount
        self.category = category.lower()
        if timestamp != "":
            datetime_obj = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
            datetime_obj= datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
            self.timestamp = datetime.strptime(datetime_obj,"%Y-%m-%d %H:%M:%S")
        else:
             self.timestamp = datetime.now(timezone.utc)    
        self.fraud = False

        return False  
    def getId(self):
        return self.id
    def getAmount(self):
        return self.amount
    def getCategory(self):
        return self.category
    def getFraud(self):
        return self.fraud  
    def getUserId(self):
        return self.user_id
    def setFraud(self,value):
        self.fraud = value
    def getTimestamp(self):
        return self.timestamp.strftime("%Y-%m-%dT%H:%M:%SZ") 
    def getTimestampDBFormat(self):
        return self.timestamp
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except Exception as e:
            print(e)
            return False   
             
        