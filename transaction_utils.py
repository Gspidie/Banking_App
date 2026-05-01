import mysql.connector
from account import local_account as local
import time 

# Future Improvement (Apr/30/2026): Connection is not closed, could result in big error!

conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "password",
    database = "banking_app"
)

cursor = conn.cursor()

def handle_fetch_balance():
    print('')
    print(f"Account Balance: ${fetch_balance(local.account_number)}")
    print('')
    time.sleep(1.5)

def handle_deposit():
    print('')
    amount = input("Enter Amount: ")
    print('')

    try:
        if float(amount) > 0:
            deposit(amount, local.account_number)
            time.sleep(1.5)
        else:
            print('')
            print("Error: Negative Amount.")
            print('')
            time.sleep(1.5)
    except:
        print('')
        print("Error: Non-Number Amount")
        print('')
        time.sleep(1.5)

def handle_withdraw():
    print('')
    amount = input("Enter Amount: ")
    print('')

    try:
        if float(amount) > 0:
            if float(amount) < fetch_balance(local.account_number):
                withdraw(amount, local.account_number)
                time.sleep(1.5)
            else:
                print('')
                print("Error: Excessive Amount.")
                print('')
                time.sleep(1.5)
        else:
            print('')
            print("Error: Negative Amount.")
            print('')
            time.sleep(1.5)
    except:
        print('')
        print("Error: Non-Number Amount")
        print('')
        time.sleep(1.5)

def handle_transfer():
    print('')
    amount = input("Enter Amount: ")
    print('')

    account_number_out = local.account_number

    print('')
    account_number_in = input("Send To Account Number: ")
    print('')

    try:
        if float(amount) > 0:
            if float(amount) < fetch_balance(local.account_number):
                transfer(amount, account_number_out, account_number_in)
                time.sleep(1.5)
            else:
                print('')
                print("Error: Excessive Amount.")
                print('')
                time.sleep(1.5)
        else:
            print('')
            print("Error: Negative Amount.")
            print('')
            time.sleep(1.5)
    except Exception as e:
        print('')
        print("Error: Non-Number Amount")
        print('')
        time.sleep(1.5)




def fetch_balance(account_number):
    query = "SELECT balance FROM accounts WHERE account_number = %s;" 
    cursor.execute(query, (account_number,))
    balance = cursor.fetchone()[0]

    conn.commit() #n

    return balance

def deposit(amount, account_number):
    try:
        conn.start_transaction()

        lock_rows([account_number])

        update_row('+', amount, account_number)

        log("Deposit", amount, None, account_number)

        conn.commit()

        print('')
        print(f"Deposited: ${amount}")
        print('')

    except:
        conn.rollback()

def withdraw(amount, account_number):
    try:
        conn.start_transaction()

        lock_rows([account_number])

        update_row('-', amount, account_number)

        log("Withdraw", amount, account_number, None)

        conn.commit()

        print('')
        print(f"Withdrew: ${amount}")
        print('')

    except:
        conn.rollback()

def transfer(amount, account_number_out, account_number_in):
    try:
        conn.start_transaction()

        lock_rows(sorted([account_number_out, account_number_in]))

        update_row('-', amount, account_number_out)
        update_row('+', amount, account_number_in)

        log("Transfer", amount, account_number_out, account_number_in)

        conn.commit()

        print('')
        print(f"Transfered: ${amount}")
        print('')
    except:
        conn.rollback()
        print(f"Error: Invalid Account Number or Failed to Transfer")

def lock_rows(account_numbers):
    placeholders = ','.join(['%s'] * len(account_numbers))
    query_lock = f"SELECT account_number FROM accounts WHERE account_number IN({placeholders}) FOR UPDATE;"
    cursor.execute(query_lock, account_numbers)

    result = cursor.fetchall()

def update_row(operator, amount, account_number):
    query_update = None

    if operator == '-':
        query_update = "UPDATE accounts SET balance = balance - %s WHERE account_number = %s;"
    else:
        query_update = "UPDATE accounts SET balance = balance + %s WHERE account_number = %s;"

    cursor.execute(query_update, (amount, account_number))

def log(operation, amount, account_number_out, account_number_in):
    query_log = "INSERT INTO transactions (operation, amount, from_account_number, to_account_number) VALUES (%s, %s, %s, %s);"
    cursor.execute(query_log, (operation, amount, account_number_out, account_number_in))
