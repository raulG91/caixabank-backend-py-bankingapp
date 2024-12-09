from werkzeug.security import generate_password_hash,check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
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
        self.balance
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
            year,month,day = start_date.split("-")
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
                    "start_date": f'{self.start_date.year}-{self.start_date.month}-{self.start_date.day}',
                    "created_at":f'{self.created_at.year}-{self.created_at.month}-{self.created_at.day}'
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
                    