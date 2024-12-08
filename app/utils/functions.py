import re
def check_email(email:str)->bool:
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is not None


def check_mandatory_fields(fields:list,dictionary:dict):
    mandatory_fields = set(fields)
    return mandatory_fields.issubset(dictionary.keys())


def add_months(dt,months):
       # Calculate the new year and month
    new_month = dt.month + months
    new_year = dt.year + (new_month - 1) // 12
    new_month = (new_month - 1) % 12 + 1
    
    # Handle day overflow (e.g., Feb 30th)
    try:
        new_date = dt.replace(year=new_year, month=new_month)
    except ValueError:
        # If the day is invalid (e.g., Feb 30), set it to the last day of the month
        if new_month == 2:
            # February
            day = 29 if (new_year % 4 == 0 and (new_year % 100 != 0 or new_year % 400 == 0)) else 28
        elif new_month in [4, 6, 9, 11]:
            # April, June, September, November
            day = 30
        else:
            # January, March, May, July, August, October, December
            day = 31
        new_date = dt.replace(year=new_year, month=new_month, day=day)
    
    return new_date