import os
import json
from datetime import datetime, timedelta

USER_FILE = 'users.json'
SESSION_FILE = 'sessions.json'
EARNINGS_FILE = 'earnings.json'

def clear_screen():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For Unix/Linux/MacOS
    else:
        os.system('clear')

clear_screen()

def initialize_files():
    for filename in [USER_FILE, SESSION_FILE, EARNINGS_FILE]:
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                json.dump([], f)

def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def register_user(username, full_name, email):
    clear_screen()
    users = load_json(USER_FILE)
    for user in users:
        if user['Username'] == username:
            print(f"User '{username}' already exists.")
            return
    user_data = {
        'Username': username,
        'Full Name': full_name,
        'Email': email
    }
    users.append(user_data)
    save_json(users, USER_FILE)
    print(f"User '{username}' registered successfully.")

def start_session(username):
    clear_screen()
    users = load_json(USER_FILE)
    sessions = load_json(SESSION_FILE)

    # Check if user is registered
    if not any(user['Username'] == username for user in users):
        print(f"User '{username}' is not registered.")
        return

    # Check if user already has an active session
    if any(session['Username'] == username for session in sessions):
        print(f"User '{username}' already has an active session.")
        return

    # Start session
    start_time = datetime.now().isoformat()
    session_data = {'Username': username, 'Start Time': start_time}
    sessions.append(session_data)
    save_json(sessions, SESSION_FILE)
    print(f"Session started for '{username}'.")

def end_session(username, rate_per_hour=15.0):
    clear_screen()
    sessions = load_json(SESSION_FILE)
    earnings = load_json(EARNINGS_FILE)

    for session in sessions:
        if session['Username'] == username:
            start_time = datetime.fromisoformat(session['Start Time'])
            end_time = datetime.now()
            duration = end_time - start_time
            total_hours = duration.total_seconds() / 3600
            total_cost = round(total_hours * rate_per_hour, 2)
            earnings_entry = {
                'Username': username,
                'Start Time': start_time.isoformat(),
                'End Time': end_time.isoformat(),
                'Duration': str(duration),
                'Earnings': total_cost
            }
            earnings.append(earnings_entry)
            sessions.remove(session)
            save_json(sessions, SESSION_FILE)
            save_json(earnings, EARNINGS_FILE)
            print(f"Session ended for user '{username}'. Total cost: ₱{total_cost}")
            return
    print(f"User '{username}' does not have an active session.")

def list_users(rate_per_hour=15.0):
    clear_screen()
    users = load_json(USER_FILE)
    sessions = load_json(SESSION_FILE)

    print("Registered users:")
    print("{:<20} {:<20} {:<20} {:<20}".format("Username", "Session Status", "Duration", "Cost"))
    print("-" * 90)

    for user in users:
        username = user['Username']
        session_status = "Active" if any(session['Username'] == username for session in sessions) else "Inactive"
        if session_status == "Active":
            start_time = next(session['Start Time'] for session in sessions if session['Username'] == username)
            start_time = datetime.fromisoformat(start_time)
            duration = datetime.now() - start_time
            duration_str = str(duration).split('.')[0]  # Convert timedelta to string
            total_hours = duration.total_seconds() / 3600
            total_cost = round(total_hours * rate_per_hour, 2)
            cost_with_symbol = f"₱{total_cost}"  # Prepend '₱' to total_cost
        else:
            duration_str = ""
            cost_with_symbol = ""
        print("{:<20} {:<20} {:<20} {:<20}".format(username, session_status, duration_str, cost_with_symbol))



def total_earnings():
    clear_screen()
    earnings = load_json(EARNINGS_FILE)
    total = sum(entry['Earnings'] for entry in earnings)
    print(f"Total earnings: ₱{total}")

def main():
    initialize_files()

    while True:
        print("\nInternet Cafe Management System")
        print("------------------------------------")
        print("[1] Register User")
        print("[2] Start Session")
        print("[3] End Session")
        print("[4] List Users")
        print("[5] Total Earnings")
        print("[6] Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Enter your username: ")
            full_name = input("Enter your full name: ")
            email = input("Enter your email: ")
            register_user(username, full_name, email)
        elif choice == '2':
            username = input("Enter the username: ")
            start_session(username)
        elif choice == '3':
            username = input("Enter the username: ")
            end_session(username)
        elif choice == '4':
            list_users()
        elif choice == '5':
            total_earnings()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

main()