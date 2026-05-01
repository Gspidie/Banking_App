import authentication_utils as au
import transaction_utils as tu 
from account import local_account as local
import time

def authenticate():
    authentication_finished = False

    while not authentication_finished:
        options = {
            "1" : au.log_in,
            "2" : au.sign_up
        }

        print("------------------------------------------")
        print("|            LOG IN | SIGN UP            |")
        print("------------------------------------------")

        print('')
        print("1) Log In")
        print("2) Sign Up")
        print('')

        print('')
        option = input("Select an option: ")
        print('')

        action = options.get(option)

        if action:
            print('')
            action()
            print('')
            authentication_finished = True
        else:
            print('')
            print("Invalid Option.")
            time.sleep(1.5)
            print('')


def transact():
    transaction_finished = False

    while not transaction_finished:
        options = {
            "1" : tu.handle_fetch_balance,
            "2" : tu.handle_deposit,
            "3" : tu.handle_withdraw,
            "4" : tu.handle_transfer
        }

        print("------------------------------------------")
        print("|               DASHBOARD                |")
        print("------------------------------------------")

        print('')
        print(f"User: {local.first_name} {local.last_name}")
        print(f"Account Number: {local.account_number}")
        print('')

        print('')
        print("1) Check Balance")
        print("2) Deposit")
        print("3) Withdraw")
        print("4) Transfer")
        print("5) Quit")
        print('')

        print('')
        option = input("Select an option: ")
        print('')

        if option == "5":
            transaction_finished = True
        else:
            action = options.get(option)

            if action:
                print('')
                action()
                print('')
            else:
                print('')
                print("Invalid Option.")
                time.sleep(1.5)
                print('')

def logo():
    print(r""" 
 ___________________________________________________________
|                                                           |
|    ___             _                     ___              |
|   |   \           | | __                |   |             |
|   |   /  __   ___ | |/ / _  ___  ___    | _ | ___  ___    |
|   |   \ /  | |   \|   \ | ||   \/   |   | | ||   \|   \   |
|   |___/ \___\|_|_||_|\_\|_||_|_||__ |   |_|_||  _/|  _/   |
|                                  _| |        | |  | |     |
|                                 |___/        |_|  |_|     |
|___________________________________________________________|
          
    """)  
