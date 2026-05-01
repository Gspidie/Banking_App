import mysql.connector
import secrets
import account as a

conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "password",
    database = "banking_app"
)

cursor = conn.cursor()


def log_in():
    access_granted = False

    id = None
    first_name = None
    last_name = None
    account_number = None

    print("------------------------------------------")
    print("|                LOG IN                  |")
    print("------------------------------------------")

    while not access_granted:
        print('')
        username = input("Enter username: ")
        password = input("Enter password: ")
        print('')

        if account_exists(username):
            id = fetch_id(username)

            if password_valid(id, password):
                access_granted = True
            else:
                print('')
                print("Invalid Password.")
                print('')
        else:
            print('')
            print("Invalid Username.")
            print('')

    first_name, last_name, account_number = fetch_account(id)

    a.local_account.id = id
    a.local_account.first_name = first_name
    a.local_account.last_name = last_name
    a.local_account.account_number = account_number

    conn.close()
    cursor.close()

def sign_up():
    account_created = False

    id = None
    first_name = None
    last_name = None
    username = None
    password = None
    account_number = None

    print("------------------------------------------")
    print("|                SIGN UP                 |")
    print("------------------------------------------")

    print('')
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    print('')

    while not account_created:
        print('')
        username = input("Enter username: ")
        print('')

        if account_exists(username):
            print('')
            print("Unavailable Username.")
            print('')
        else:
            print('')
            password = input("Enter password: ")
            print('')
            account_number = generate_account_number()
            id = create_account(first_name, last_name, username, password, account_number)
            account_created = True

    a.local_account.id = id
    a.local_account.first_name = first_name
    a.local_account.last_name = last_name
    a.local_account.account_number = account_number

    conn.close()
    cursor.close()


def account_exists(username):
    query = "SELECT EXISTS (SELECT 1 FROM accounts WHERE username = %s)"
    cursor.execute(query, (username,))
    result = cursor.fetchone()[0]

    conn.commit() #n

    if result == 1:
        return True
    else: 
        return False

def fetch_id(username):
    query = "SELECT id FROM accounts WHERE username = %s"
    cursor.execute(query, (username,))
    account_id = cursor.fetchone()[0]

    conn.commit() #n

    return account_id

def password_valid(id, password):
    query = "SELECT (user_password = %s) FROM accounts WHERE id = %s"
    cursor.execute(query, (password, id))
    result = cursor.fetchone()[0]

    conn.commit() #n

    if result == 1:
        return True
    else:
        return False
    
def fetch_account(id):
    query = "SELECT first_name, last_name, account_number FROM accounts WHERE id = %s"
    cursor.execute(query, (id,))
    account = cursor.fetchone()

    conn.commit() #n

    return account 
    
def generate_account_number():
    valid_account_number = False
    account_number = ""

    digits = '0123456789'

    while not valid_account_number:

        for i in range(10):
            digit = secrets.choice(digits)
            account_number += digit

        if account_number_exists(account_number):
            account_number = ""
        else:
            valid_account_number = True

    return account_number

def account_number_exists(account_number):
    query = "SELECT EXISTS (SELECT 1 FROM accounts WHERE account_number = %s)"
    cursor.execute(query, (account_number,))
    result = cursor.fetchone()[0]

    conn.commit() #n

    if result == 1:
        return True
    else: 
        return False

def create_account(first_name, last_name, username, password, account_number):
    query = "INSERT INTO accounts (first_name, last_name, username, user_password, account_number) VALUES (%s, %s, %s, %s, %s);"
    cursor.execute(query, (first_name, last_name, username, password, account_number))
    conn.commit()

    query = "SELECT LAST_INSERT_ID();"
    cursor.execute(query)
    id = cursor.fetchone()[0]

    conn.commit() #n

    return id
