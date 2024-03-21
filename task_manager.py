# Notes:
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

# Importing necessary libraries
import os
from datetime import datetime, date

# Date format used for parsing and displaying dates
DATETIME_STRING_FORMAT = "%Y-%m-%d"

def read_tasks_from_file():
    """Reads tasks from tasks.txt file and returns a list of task dictionaries."""
    # Create tasks.txt if it doesn't exist with a default task
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as default_file:
            default_file.write("admin;Add functionality to task manager;Add additional options and refactor the code.;2022-12-01;2022-11-22;No")

    # Read tasks from file and convert to list of dictionaries
    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    task_list = []
    for t_str in task_data:
        curr_t = {}
        task_components = t_str.split(";")
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
        curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        curr_t['completed'] = True if task_components[5] == "Yes" else False
        task_list.append(curr_t)

    return task_list

def write_tasks_to_file(task_list):
    """Writes the updated task list to tasks.txt file."""
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

def add_task():
    """Handles the logic for adding a new task."""
    task_list = read_tasks_from_file()

    task_username = input("Name of person assigned to task: ")
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")

    # Validate and parse the due date
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Create the new task dictionary
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": date.today(),
        "completed": False
    }

    # Add the new task to the task list and write back to file
    task_list.append(new_task)
    write_tasks_to_file(task_list)
    print("Task successfully added.")

def display_task(task):
    """Displays details of a single task."""
    print("Task:", task['title'])
    print("Assigned to:", task['username'])
    print("Date Assigned:", task['assigned_date'].strftime(DATETIME_STRING_FORMAT))
    print("Due Date:", task['due_date'].strftime(DATETIME_STRING_FORMAT))
    print("Task Description:")
    print(task['description'])
    print()

def display_all_tasks():
    """Displays all tasks in the task list."""
    task_list = read_tasks_from_file()
    for task in task_list:
        display_task(task)

def main():
    """Main function to manage the task manager."""
    while True:
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
            register_user()
        elif menu == 'a':
            add_task()
        elif menu == 'va':
            display_all_tasks()
        elif menu == 'vm':
            display_user_tasks()
        elif menu == 'ds':
            display_statistics()
        elif menu == 'e':
            print('Goodbye!!!')
            break
        else:
            print("You have made a wrong choice. Please try again.")

if __name__ == "__main__":
    main()

