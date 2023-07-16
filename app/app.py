import mysql.connector
from flask import Flask, render_template, request, redirect
from datetime import datetime

app = Flask(__name__)

# Database connection configuration
db_config = {
    'host': 'db',
    'user': 'root',
    'password': 'root',
    'database': 'bank',
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

connection = get_db_connection()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        choice = request.form.get('choice')
        if choice == '1':
            return redirect('/signup')
        elif choice == '2':
            return redirect('/login')
        elif choice != '2':
            return render_template('index.html', warning='Please enter either 1 or 2.')
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        dob = request.form.get('dob')
        mobile = request.form.get('mobile')
        amount = request.form.get('amount')
        connection = get_db_connection()

        # Perform database operations (e.g., insert new user data)
        cursor = connection.cursor()
        sql = "INSERT INTO users (name, username, password, dob, mobile, amount) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (name, username, password, dob, mobile, amount)
        cursor.execute(sql, values)

        # Commit the transaction and close the connection
        connection.commit()
        connection.close()

        # Redirect to a success page or perform further actions
        return redirect('/signup_success')

    return render_template('signup.html')

@app.route('/signup_success')
def signup_success():
    return render_template('signup_success.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(sql, (username, password))
        user = cursor.fetchone()
        if user is None:
            return "Invalid username or password. Please try again"
        # Redirect to the homepage
        return redirect(f'/homepage.html?username={username}')

    return render_template('login.html')

@app.route('/homepage.html', methods=['GET', 'POST'])
def homepage():
    username = request.args.get('username')
    if request.method == 'POST':
        user_choice = request.form.get('user-choice')
        username = request.form.get('username')
        if user_choice == '1':
            return redirect(f'/withdraw.html?username={username}')
        elif user_choice == '2':
            return redirect(f'/deposit.html?username={username}')
        elif user_choice == '3':
            return redirect(f'/transactions.html?username={username}')
        elif user_choice == '4':
            return redirect('/logout')
    return render_template('homepage.html', username=username)

@app.route('/withdraw.html', methods=['GET', 'POST'])
def withdraw():
    if request.method == 'POST':
        username = request.form.get('username')
        withdrawal_amount = request.form.get('amount')
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = "SELECT amount FROM users WHERE username = %s"
        cursor.execute(sql, (username,))
        result = cursor.fetchone()
        if result is None:
            return "Invalid username. Please try again"
        current_balance = float(result[0])
        new_balance = current_balance - float(withdrawal_amount)
        if new_balance < 0:
            return "Insufficient balance. Please try again"
        sql = "UPDATE users SET amount = %s WHERE username = %s"
        cursor.execute(sql, (new_balance, username))
        connection.commit()
        transaction_date = datetime.now()
        insert_transaction_query = "INSERT INTO transactions (transaction_type, amount, transaction_date, balance, user) VALUES (%s, %s, %s, %s, %s)"
        transaction_data = ('Debit', withdrawal_amount, transaction_date, new_balance, username)
        cursor.execute(insert_transaction_query, transaction_data)
        connection.commit()
        return render_template('withdraw_success.html', amount=withdrawal_amount, username=username)
    username = request.args.get('username')
    sql = "SELECT amount FROM users WHERE username = %s"
    cursor.execute(sql, (username,))
    result = cursor.fetchone()
    if result is None:
        return "Invalid username. Please try again"
    balance = result[0]
    return render_template('withdraw.html', balance=balance, username=username)

@app.route('/deposit.html', methods=['GET', 'POST'])
def deposit():
    if request.method == 'POST':
        username = request.form.get('username')
        deposit_amount = request.form.get('amount')
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = "SELECT amount FROM users WHERE username = %s"
        cursor.execute(sql, (username,))
        result = cursor.fetchone()
        if result is None:
            return "Invalid username. Please try again"
        current_balance = float(result[0])
        new_balance = current_balance + float(deposit_amount)
        sql = "UPDATE users SET amount = %s WHERE username = %s"
        cursor.execute(sql, (new_balance, username))
        connection.commit()
        transaction_date = datetime.now()
        insert_transaction_query = "INSERT INTO transactions (transaction_type, amount, transaction_date, balance, user) VALUES (%s, %s, %s, %s, %s)"
        transaction_data = ('Credit', deposit_amount, transaction_date, new_balance, username)
        cursor.execute(insert_transaction_query, transaction_data)
        connection.commit()
        return render_template('deposit_success.html', amount=deposit_amount, username=username)
    username = request.args.get('username')
    sql = "SELECT amount FROM users WHERE username = %s"
    cursor.execute(sql, (username,))
    result = cursor.fetchone()
    if result is None:
        return "Invalid username. Please try again"
    balance = result[0]
    return render_template('deposit.html', balance=balance, username=username)

@app.route('/transactions.html')
def transactions():
    username = request.args.get('username')
    connection = get_db_connection()
    cursor = connection.cursor()
    sql = "SELECT * FROM transactions WHERE user = %s"
    cursor.execute(sql, (username,))
    transactions = cursor.fetchall()
    return render_template('transactions.html', username=username, transactions=transactions)

@app.route('/logout')
def logout():
    return render_template('logout.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)
