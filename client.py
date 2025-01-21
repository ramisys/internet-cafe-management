import json, os
from datetime import datetime

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

def load_json(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_json(data, filename):
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"Error saving data to {filename}: {e}")

def login(users, username):
    clear_screen()
    if any(user['Username'] == username for user in users):
        print(f"Welcome, {username}!")
        return username
    else:
        print("Invalid username.")
        return None

def start_session(username):
    clear_screen()
    sessions = load_json(SESSION_FILE)
    if any(session['Username'] == username for session in sessions):
        print(f"User '{username}' already has an active session.")
        return
    start_time = datetime.now().isoformat()
    session_data = {'Username': username, 'Start Time': start_time}
    sessions.append(session_data)
    save_json(sessions, SESSION_FILE)
    print("Session started.")

def view_session(username):
    clear_screen()
    sessions = load_json(SESSION_FILE)
    for session in sessions:
        if session['Username'] == username:
            start_time = datetime.fromisoformat(session['Start Time'])
            duration = datetime.now() - start_time
            total_hours = duration.total_seconds() / 3600
            total_cost = round(total_hours * 15, 2)  # Assuming rate per hour is ₱15
            print(f"Session Duration: {duration}, Total Cost: ₱{total_cost}")
            return
    print("No active session found.")

def logout(username):
    clear_screen()
    sessions = load_json(SESSION_FILE)
    earnings = load_json(EARNINGS_FILE)

    for session in sessions:
        if session['Username'] == username:
            start_time = datetime.fromisoformat(session['Start Time'])
            end_time = datetime.now()
            duration = end_time - start_time
            total_hours = duration.total_seconds() / 3600
            total_cost = round(total_hours * 15, 2)  # Assuming rate per hour is ₱15

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
            print("Logged out successfully.")
            return
    print("No active session found.")

def main():
    users = load_json(USER_FILE)
    logged_in_user = None

    while True:
        if logged_in_user is None:
            print("\nInternet Cafe Client System")
            username = input("Enter your username: ")
            logged_in_user = login(users, username)
        else:
            print(f"\nInternet Cafe Client System - Logged in as {logged_in_user}")
            print("------------------------------------")
            print("[1] Start Session")
            print("[2] View Session")
            print("[3] Logout")
            print("[4] Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                start_session(logged_in_user)
            elif choice == '2':
                view_session(logged_in_user)
            elif choice == '3':
                logout(logged_in_user)
                logged_in_user = None
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()