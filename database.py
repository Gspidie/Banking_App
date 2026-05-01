import mysql.connector

conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "password",
    database = "banking_app"
)

cursor = conn.cursor()


def setup_database():
    try:
        conn.start_transaction()

        cursor.execute("USE banking_app;")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INT PRIMARY KEY AUTO_INCREMENT,
                first_name VARCHAR(64) NOT NULL,
                last_name VARCHAR(64) NOT NULL,
                username VARCHAR(64) NOT NULL UNIQUE,
                user_password VARCHAR(64) NOT NULL,
                account_number VARCHAR(64) NOT NULL UNIQUE,
                balance DECIMAL(7,2) NOT NULL DEFAULT '0.00'
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INT PRIMARY KEY AUTO_INCREMENT,
                operation VARCHAR(64) NOT NULL,
                amount DECIMAL(7,2),
                from_account_number VARCHAR(64),
                to_account_number VARCHAR(64),
                date_logged DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (from_account_number) REFERENCES accounts(account_number),
                FOREIGN KEY (to_account_number) REFERENCES accounts(account_number)
            );
        """)

        query = "INSERT INTO accounts (first_name, last_name, username, user_password, account_number) VALUES (%s, %s, %s, %s, %s)"

        cursor.execute(query, ("t_first_name", "t_last_name", "t_username", "t_password", "0000000000"))

        conn.commit()

    except:
        conn.rollback()

    conn.close()
    cursor.close()

setup_database()
