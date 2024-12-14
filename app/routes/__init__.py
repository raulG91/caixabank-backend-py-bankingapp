from flask import Blueprint

user_bp=Blueprint('users',__name__,url_prefix='/api/auth')
expenses_bp = Blueprint('expenses',__name__,url_prefix='/api/recurring-expenses')
transfers_bp= Blueprint('transfers',__name__,url_prefix='/api/transfers')
alerts_bp = Blueprint('alerts',__name__,url_prefix='/api/alerts')
transaction_bp = Blueprint('transactions',__name__,url_prefix='/api')

from . import user_routes,expenses_recurring_routes,transfers_routes,alerts_routes,transactions_routes