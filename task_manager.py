# Notes:
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

# Importing necessary libraries
import os
from datetime import datetime, date

# Format for datetime strings
DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        default_file.write("admin;Add functionality to task manager;Add additional options and refactor the code.;2022-12-01;2022-11-22;No")

# Read tasks from tasks.txt and create a list of dictionaries
with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

task_list = []
for t_str in task_data:
    curr_t = {}

    # Splitting by semicolon and adding components to dictionary
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)

# Login Section
'''This code reads usernames and passwords from the user.txt file to 
allow a user to login.'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read user_data from user.txt
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary for easy access
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:
    # Login prompt
    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

while True:
    # Menu for user interaction
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        '''Add a new user to the user.txt file'''
        # Get inputs for new user
        new_username = input("New Username: ")
        new_password = input("New Password: ")
        confirm_password = input("Confirm Password: ")

        # Check if passwords match
        if new_password == confirm_password:
            print("New user added")
            username_password[new_username] = new_password
            
            # Write updated user data to user.txt
            with open("user.txt", "w") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))

        else:
            print("Passwords do not match")

    elif menu == 'a':
        '''Allow a user to add a new task to tasks.txt file'''
        # Get inputs for new task
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            continue
        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")
        
        # Get due date of task
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break
            except ValueError:
                print("Invalid datetime format. Please use the format specified")

        # Add new task to task_list
        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": date.today(),
            "completed": False
        }

        task_list.append(new_task)
        
        # Write updated task data to tasks.txt
        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))
        print("Task successfully added.")

    elif menu == 'va':
        '''Reads and displays all tasks from tasks.txt'''
        for t in task_list:
            disp_str = f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)

    elif menu == 'vm':
        '''Reads and displays tasks assigned to the logged-in user'''
        for t in task_list:
            if t['username'] == curr_user:
                disp_str = f"Task: \t\t {t['title']}\n"
                disp_str += f"Assigned to: \t {t['username']}\n"
                disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Task Description: \n {t['description']}\n"
                print(disp_str)

    elif menu == 'ds' and curr_user == 'admin': 
        '''Displays statistics about users and tasks for admin user'''
        num_users = len(username_password.keys())
