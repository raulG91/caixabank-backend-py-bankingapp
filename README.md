# 🏦 Python Backend Challenge - Financial APP 🐍

Category   ➡️   Software

Subcategory   ➡️   Python Backend

Difficulty   ➡️   Medium

Average solution time ➡️ 3 hours. The timer will begin when you click the start button and will stop upon your submission.

---

## 🌐 Background
CaixaBank is driving the development of a new digital platform aimed at enhancing financial management for its clients while ensuring transaction security. The goal is to provide tools that enable customers to manage their accounts in a personalized and efficient manner, alongside mechanisms to detect unusual financial behaviors.

As a developer, your mission is to create a backend API that implements key functionalities related to account management, simulation of financial operations, and the detection of suspicious patterns in clients' spending habits.


## 📂 Repository Structure
```
financial_management_app/
├── app/
│   ├── __init__.py          
│   ├── config.py             
│   ├── models.py             
│   ├── routes/
│   │   └──...    
│   ├── services/
│   │   └── ...    
│   ├── utils/
│   │   └── ...   
│   ├── exchange_fees.csv
│   └── exchange_rates.csv
├── Dockerfile                
├── docker-compose.yml        
├── requirements.txt          
└── README.md                 
```
## 🎯 Tasks

#### TASK 1: Manage user login

Develop a simple user authentication functionality for the digital financial management platform. This involves implementing secure and efficient mechanisms to register users and manage their login sessions. The authentication system must use JWT (JSON Web Tokens) for session management and ensure that user passwords are securely stored using hashing techniques.


- Authentication Endpoints

| Endpoint                         | Method | Params/Body                                                                                  | Requires Auth | Response Codes              |
|----------------------------------|--------|---------------------------------------------------------------------------------------------|---------------|-----------------------------|
| `/api/auth/register`                 | POST   | `{ "email": string, "password": string, "name": string }`                                   | No            | 201 (Created), 400 (Error)  |
| `/api/auth/login`                    | POST   | `{ "email": string, "password": string }`                                                  | No            | 200 (OK), 400 (Error), 401 (Unauthorized) |

 - Expected responses:

| **Endpoint**        | **/api/auth/register**                                                                                           |
|----------------------|-------------------------------------------------------------------------------------------------------------|
| **Response**         | **201 - Success:**   ```{"name":"Nuwe Test","hashedPassword":"$2b$12$ia0DtGN3VcWSAMG0zwQ/JuYCT.E921nXv6ttbQSzhXhDh1YEBNXIW","email": "nuwe@nuwe.com"}```     |
| **Error Responses**  | **400 - Invalid email:** ```Invalid email: nuwe#nuwe.com```                                                |
|                      | **400 - Email already exists:** ```Email already exists.```                                                |
|                      | **400 - Missing data:** ```All fields are required.```                                                     |
|                      | **400 - Null fields:** ```No empty fields allowed.```                                                      |

| **Endpoint**         | **/api/auth/login**                                                                                            |
|----------------------|-------------------------------------------------------------------------------------------------------------|
| **Response**         | **200 - Success:**   ```{"token": (JWT token) }```                                                           |
| **Error Responses**  | **400 - User not found:** ```User not found for the given email: (email)```                               |
|                      | **401 - Password does not match:** ```Bad credentials.```                                                |
|                      | **401 - Null fields:** ```Bad credentials.```                                                      |



#### TASK 2: Projection of Recurring Expenses

Develop the endpoints needed to allow customers to input their recurring monthly expenses, such as subscriptions, bills, and loan payments. Manage both positive (inflows) and negative (outflows) amounts. The system will then calculate the cumulative effect of these expenses on their balance over the course of a year. The response should include a detailed breakdown showing how each recurring expense affects their monthly and yearly balances. Ensure the system is designed to handle changes in expenses or additional costs, and JWT for secure user authentication, ensuring that only authorized users can access their financial projections. 



- Table endpoints to implement

| Endpoint                               | Method | Params/Body                                                                                                                                                    | Requires Auth** | Response Codes                  | Description                                                                 |
|-----------------------------------------|------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|-------------------------------|---------------------------------------------------------------------------------|
| `/api/recurring-expenses`               | `POST`     | Body: `{"expense_name": "TV Subscription", "amount": 12.99, "frequency": "monthly", "start_date": "2024-01-01"}`                                          | Yes               | 201 Created, 400 Bad Request  | Creates a new recurring expense for the user.                                    |
| `/api/recurring-expenses`               | `GET`      | None                                                                                                                                                      | Yes               | 200 OK, 401 Unauthorized      | Retrieves the list of all recurring expenses for the authenticated user.        |
| `/api/recurring-expenses/{expense_id}`  | `PUT`      | Body: `{"expense_name": "Music Subscription", "amount": 15.99, "frequency": "monthly", "start_date": "2024-01-01"}`                               | Yes               | 200 OK, 400 Bad Request, 404 Not Found | Updates an existing recurring expense identified by `expense_id`.                |
| `/api/recurring-expenses/{expense_id}`  | `DELETE`   | Params: `{expense_id}`                                                                                                                                    | Yes               | 200 OK, 404 Not Found         | Deletes a recurring expense identified by `expense_id`.                          |
| `/api/recurring-expenses/projection`    | `GET`      | None                                                                                                                                                      | Yes               | 200 OK, 401 Unauthorized      | Provides a detailed month-by-month projection of the user's balance. Returns de following 12 months.            |

- Endpoint Response messages expected:

| **Endpoint**         | **/api/recurring-expenses  [POST]**                                                                                       |
|----------------------|-------------------------------------------------------------------------------------------------------------|
| **Response**         | **201 - Success**   ```{"msg":"Recurring expense added successfully.","data":{"id": ..., "expense_name": ..., "amount": .., "frequency": ..., "start_date": ...}}```                                                           |
| **Error Responses**  | **400 - Data not provided:** ```{"msg": "No data provided."}```                             |
|                      | **400 - Null fields:** ```{"msg": "No empty fields allowed"}.```                                                 |

| **Endpoint**         | **/api/recurring-expenses [GET]**                                                                                             |
|----------------------|-------------------------------------------------------------------------------------------------------------|
| **Response**         | **200 - Success**   ```list of transactions```                                                           |

| **Endpoint**         | **/api/recurring-expenses/{expense_id}  [PUT]**                                                                                       |
|----------------------|-------------------------------------------------------------------------------------------------------------|
| **Response**         | **200 - Success**   ```{"msg": "Recurring expense updated successfully.","data":{"id": ..., "expense_name": ..., "amount": .., "frequency": ..., "start_date": ...}}```                                                           |
| **Error Responses**  | **400 - Data not provided:** ```{"msg": "No data provided."}```                          |
|                      | **400 - Null fields:** ```{"msg": "No empty fields allowed."}.```                                               |
|                      | **404 - Expense id not found:** ```{"msg": "Expense not found."}```                                                          |

| **Endpoint**         | **/api/recurring-expenses/{expense_id}  [DELETE]**                                                                                    |
|----------------------|-------------------------------------------------------------------------------------------------------------|
| **Response**         | **200 - Success**   ```{"msg":  "Recurring expense deleted successfully."}```                                                           |
| **Error Responses**  | **404 - Expense id not found:** ```{"msg": "Expense not found."}```                                |

| **Endpoint**         | **/api/recurring-expenses/projection  [GET]**                                                                                    |
|----------------------|-------------------------------------------------------------------------------------------------------------|
| **Response**         | **200 - Success**   ``` list of monthly expenses [{"month":YYYY-MM,"recurring_expenses" : float (total amount)} , {...} , ...]```                                                           |


#### TASK 3: Simulation of International Transfers:
Implement a feature where users can simulate international money transfers, calculating the exchange rate, applicable fees, and the final amount the recipient will receive in the destination currency. Calculate the total cost of the transfer, including exchange rates, and return the amount the recipient will receive. Use JWT to verify the user's identity before allowing them access to the simulation. 
- The currencies exchanges and fees can be found in the files `exchange_rates.csv`and `exchange_fees.csv`.

- Table endpoints:

| Endpoint                           | Method | Params / Body                                                   | Requires Auth | Response Codes          | Description                                                                                                    |
|------------------------------------|--------|------------------------------------------------------------------|---------------|--------------------------|------------------------------------------------------------------------------------------------|
| `/api/transfers/simulate`          | POST   | **Body:** `{ "amount": float, "source_currency": str, "target_currency": str }` | Yes           | 201 OK, 400 Bad Request  | Simulates an international transfer, calculating the amount in `target_currency` after exchange rates and fees are applied. Formula: `target_currency`= `source_currency`×(1−fee)×rate|
| `/api/transfers/fees`              | GET    | **Params:** `source_currency`, `target_currency`                | Yes           | 200 OK, 400 Bad Request  | Retrieves information on applicable fees for a transfer between `source_currency` and `target_currency`. |
| `/api/transfers/rates`             | GET    | **Params:** `source_currency`, `target_currency`                | Yes           | 200 OK, 400 Bad Request  | Retrieves the current exchange rate between `source_currency` and `target_currency`. |


| **Endpoint**         | **/api/transfers/simulate**                                                                                       |
|----------------------|-------------------------------------------------------------------------------------------------------------|
| **Response**         | **201 - Success**   ```{"msg": "Amount in target currency: {total_amount}."}```                                                           |
| **Error Responses**  | **400 - Null fields:** ```{"msg": "No empty fields allowed."}.```                       |
|                      | **404 - Currencies not found:** ```{"msg": "Invalid currencies or no exchange data available."}```

| **Endpoint**         | **/api/transfers/fees**                                                                                       |
|----------------------|-------------------------------------------------------------------------------------------------------------|
| **Response**         | **200 - Success**   ```{"fee": float}```                                                           |
| **Error Responses**  | **400 - Null fields:** ```{"msg": "No empty fields allowed."}.```                       |
|                      | **404 - Currencies not found:** ```{"msg": "No fee information available for these currencies."}```|

| **Endpoint**         | **/api/transfers/rates**                                                                                       |
|----------------------|-------------------------------------------------------------------------------------------------------------|
| **Response**         | **200 - Success**   ```{"rate": float}```                                                           |
| **Error Responses**  | **400 - Null fields:** ```{"msg": "No empty fields allowed."}.```                       |
|                      | **404 - Currencies not found:** ```{"msg": "No exchange rate available for these currencies."}```|


#### TASK 4: Savings Goal Alert System:
Create an API that helps customers monitor their savings goals. Create the endpoints to create and manage these alerts. User JWT for secure user authentication.

 - Table for endpoints:

| Endpoint                           | Method   | Params / Body                                                 | Requires Auth | Response Codes               | Description                                                                                      |
|----------------------------------|----------|-----------------------------------------------------------------|---------------|------------------------------|--------------------------------------------------------------------------------------------------|
| `/api/alerts/amount_reached`     | POST     | **Body:** `{ "target_amount": float, "alert_threshold":float }` | Yes           | 201 Created, 400 Bad Request | Creates a new savings goal for the user with a specified target amount and alert threshold.             |
| `/api/alerts/balance_drop`       | POST     | **Body:** `{  "balance_drop_threshold": float }`                | Yes           | 201 Created, 400 Bad Request | Creates and alert for the user when the balance diminishes in the defined amount at `balance_drop_threshold` . |
| `/api/alerts/delete`             | POST     | **Body:** `{ "alert_id": int }`                                 | Yes           | 200 OK, 404 Not Found        | Deletes the user's alerts given an `alert_id`.                                           |
| `/api/alerts/list`               | GET      | None                                                            | Yes           | 200 OK                       | Retrieves a list of all alerts for the authenticated user, along with progress and alert status. |

- Endpoint Response messages expected:

| **Endpoint**         | **/api/alerts/amount_reached  [POST]**                                                                                       |
|----------------------|-------------------------------------------------------------------------------------------------------------|
| **Response**         | **201 - Success**   ```{"msg": "Correctly added savings alert!", "data":{"id": ... ,"user_id":..., "target_amount": ..., "alert_threshold": ... }}```                                                           |
| **Error Responses**  | **400 - Null fields:** ```{"msg": "No empty fields allowed."}.```                       |


| **Endpoint**         | **/api/alerts/balance_drop  [POST]**                                                                                       |
|----------------------|-------------------------------------------------------------------------------------------------------------|
| **Response**         | **201 - Success**   ```{"msg": "Correctly added balance drop alert!", "data":{"id": ... ,"user_id":..., "balance_drop_threshold": ...}}```                                                     |
| **Error Responses**  | **400 - Null fields:** ```{"msg": "No empty fields allowed."}.```                       |


| **Endpoint**         | **/api/alerts/delete  [POST]**                                                                                       |
|----------------------|-------------------------------------------------------------------------------------------------------------|
| **Response**         | **200 - Success**   ```{"msg": "Alert deleted successfully."}```                                                           |
| **Error Responses**  | **400 - Null fields:** ```{"msg": "No empty fields allowed."}.```                       |
|                      | **400 - Missing alert ID:** ```{"msg": "Missing alert ID."}```|
|                      | **404 - Alert id not found:** ```{"msg": "Alert not found."}```|

| **Endpoint**         | **/api/alerts/list  [GET]**                                                                                       |
|----------------------|-------------------------------------------------------------------------------------------------------------|
| **Response**         | **200 - Success**   ```{"data": [{"id":... ,"user_id":..., "target_amount": ... "alert_threshold":...,"balance_drop_threshold":...}]}```                                                           |



#### TASK 5: Find Unusual patterns
Implement a set of rules to analyze a user's transaction history to identify unusual spending patterns. The system should flag transactions that deviate significantly from their typical spending behavior, for that purpose, below are the fraud detection rules you will have to implement. Additionally, JWT will be used for secure user authentication, ensuring only the authorized user can view their financial data. 


**Fraud Detection Rules**

- High Deviation from Average Spending:
Flag a transaction as fraud (fraud=True) if the amount exceeds 3 standard deviations from the customer's average daily spending over the 90 days prior to the transaction.

- Unusual Spending Category:
Flag as fraud if the transaction occurs in a category not used by the customer in the 6 months prior to the transaction.

- Rapid Transactions:
Flag as fraud if more than 3 transactions occur within 5 minutes, and the combined value exceeds the customer's daily average spend.


- Table of endpoints:

| Endpoint                  | Method | Params/Body                                                                                                         | Requires Auth** | Response Codes                     | Description                                                                 |
|---------------------------|--------|---------------------------------------------------------------------------------------------------------------------|-----------------|-----------------------------------|-----------------------------------------------------------------------------|
| `/api/transactions`       | `POST` | Body: `{"user_id": 123, "amount": 150.50, "category": "electronics", "timestamp": "2024-11-20T10:30:00Z"}` | Yes             | 201 Created, 400 Bad Request      | Adds a new transaction, evaluates it for fraud, and stores it in the database. |

- If not provided, timestamp should default to current time.
- The total balance of the user must be updated after each processed transaction.



| **Endpoint**         | **/api/transactions**                                                                                       |
|----------------------|-------------------------------------------------------------------------------------------------------------|
| **Response**         | **201 - Success**   ```{"msg": "Transaction added and evaluated for fraud.","data":{'id': ... , 'user_id':... , 'amount': .... , 'category':..., "timestamp": ... , "fraud" : ...}}```                                                           |
| **Error Responses**  | **400 - Null fields:** ```{"msg": "No empty fields allowed."}.```                       |
|                      | **400 - Missing data:** ```{"msg": "No data provided."}```|



#### TASK 6: Notify alerts via mail
Implement a feature to notify users via email when a transaction triggers one of their saved alerts. Trigger email notifications automatically when, **after a transaction**, a saved alert is matched.
Personalize emails by dynamically populating `{user_name}`, `{alert_target_amount}`, and `{alert_balance_drop_threshold}` with the relevant user and alert details.
Ensure email delivery through proper configuration of the mail server and integration with the system.
The system should generate and send email notifications using the following templates based on the type of alert:

- Template savings alert:

```
Dear {user_name},

Great news! Your savings are nearing the target amount of {alert_target_amount}.
Keep up the great work and stay consistent!

Best Regards,
The Management Team
        
```

- Template balance drop alert:

```
Dear {user_name},

We noticed a significant balance drop in your account more than {alert_balance_drop_threshold}.
If this wasn't you, please review your recent transactions to ensure everything is correct.

Best Regards,
The Management Team
        
```


### 💫 Guides
- Technology Stack: Use Python, Flask, MySQL, and Docker for the implementation.

- Docker Configuration:

    - The provided `docker-compose.yml` file will set up the necessary environment.
    - Ensure your application runs inside a Docker container and is exposed on port 3000 for API interactions during testing.
    - Dockerfile Setup: Write a `Dockerfile` to build and run your Flask application, ensuring compatibility with the provided `docker-compose.yml`.

- Database Requirements: The database must include the following tables:

    - users: To store user information such as credentials and account details.
    - alerts: To manage savings targets and balance drop thresholds.
    - recurring_expenses: For tracking recurring payments and their schedules.
    - transactions: To log financial operations and detect unusual activity.
- Ensure your API can interact seamlessly with the database and follows best practices for security, scalability, and maintainability.

Database tables schema:
```
## `users`
| Column Name       | Type          |
|-------------------|---------------|
| id                | Integer       |
| name              | String(128)   |
| email             | String(128)   |
| hashed_password   | String(128)   |
| balance           | Float         |

---

## `alerts`
| Column Name            | Type          |
|------------------------|---------------|
| id                     | Integer       |
| user_id                | Integer       |
| target_amount          | Float         |
| alert_threshold        | Float         |
| balance_drop_threshold | Float         |
| created_at             | DateTime      |

---

## `recurring_expenses`
| Column Name   | Type          |
|---------------|---------------|
| id            | Integer       |
| user_id       | Integer       |
| expense_name  | String(255)   |
| amount        | Float         |
| frequency     | String(50)    |
| start_date    | DateTime      |
| created_at    | DateTime      |

---

## `transactions`
| Column Name   | Type          |
|---------------|---------------|
| id            | Integer       |
| user_id       | Integer       |
| amount        | Float         |
| category      | String(255)   |
| timestamp     | DateTime      |
| fraud         | Boolean       |

```

## 📤 Submission
1. Solve the proposed tasks.
2. Continuously push the changes you have made.
3. Wait for the results.
4. Click submit challenge when you have reached your maximum score.

## 📊 Evaluation

The final score will be given according to whether or not the objectives have been met.

In this case, the challenge will be evaluated on 2000 (1600 for tasks and 400 for code quality) points which are distributed as follows:

- Task 1: 200 points
- Task 2: 300 points
- Task 3: 250 points
- Task 4: 300 points
- Task 5: 350 points
- Task 6: 200 points
- Code quality: 400 points

## ❓ Additional information
**Q1: Can I change anything in the app?**

A1: Yes, as the app is dockerised, you are free to modify anything within the project. But keep in mind that the endpoints will be tested against the port 3000 and they must have the specified format. 

**Q2: Can I add resources that are not in requirements.txt?**

A2: Yes, new resources can be added if necessary. Remember to add them to the `requirements.txt` file.

## Installation

In file  `config.py` you will need to set up your `SECRET_KEY` and `JWT_TOKEN` values. 
Since the application is dockerised, only needs to execute `docker compose up -d` and it will generate necessary docker images. After generating docker images, you can use the API.