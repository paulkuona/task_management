#=====importing libraries===========
from datetime import datetime
from textwrap import dedent

def get_num(prompt):
    """
    This function uses defensive programming to restrict user input to positive integers only
    on which mathematical operations can be performed by checking if the input can be cast
    to an int and returns the input as an int.
    """

    while True:
        try: 
            num = input(prompt)
            num = int(num)
            return int(num)

        except:
            print("Oops! Looks like you entered something other than a positive whole number. Try again.")   

def reg_user(current_user):
    """
    This function takes the logged in username as an argument (to check permission)
    and then allows the user to register a new user only if they are the admin. 
    The function also checks if the new username already exists in the users txt file.
    """
    
    if current_user == "admin":
        print("\n", "*"*20, " NEW USER REGISTRATION ", "*"*20, "\n")
        existing_users_lst =[] # Used to check if new username doesn't exist
        while True:
            # Checking if username already exists 
            # Asking user to enter a different username entry already exists
            new_user = input("\nEnter a new username: ").lower()

            with open('user.txt', 'r') as users_file:
                contents = users_file.readlines()

                for line in contents:
                    existing_user, _ = line.strip().split(", ")
                    existing_users_lst.append(existing_user.lower())

            # Checking if new_user exists in user.txt file and looping if it does,
            # otherwise break loop
            if new_user in existing_user:
                print("That username is already taken! Try again.")
                continue
            else:
                break

        while True:
            # Checking if password and and confirmation password match
            # and looping if they don't

            new_password = input("Create a password: ")
            password_confirm = input("Confirm your password (it should match the password)" \
                " you created): ")
            
            if new_password == password_confirm:
                with open('user.txt', 'a') as user_file:
                    user_credentials ="\n" + new_user + ", " + new_password
                    user_file.write(user_credentials)
                    print("\nThe new user account has been created!\n")
                    break
            else:
                print("\nThe passwords you entered do not match! Please try again.\n")
    
    # ====Denying new user registration if not admin====
    else:
        print("\nYou are not authorised to register new users! Please choose another option")

def add_task():
    """
    This function allows a user to create a task for another registered user.
    """


    print("\n", "*"*20, " ADD A NEW TASK ", "*"*20, "\n")
    while True:
        # Checking if selected user exists in user.txt file and looping and asking for existing user
        # if selected user doesn't exist.

        select_user = input("Enter the username of the person to whom the task is assigned: ").lower()
        users = []
        with open('user.txt', 'r') as user_file:
            # extracting usernames from user.txt file

            credentials = user_file.readlines()

            for line in credentials:
                user, _ = line.strip().split(", ")
                users.append(user.lower())

        # Checking if select_user exists in user.txt
        if select_user in users:
            # Getting task details if select_user exists

            assignee = select_user
            task_title = input("Give your task a title: ")
            task_description = input("Describe this task: ")
            assignment_date = datetime.today().strftime("%d %b %Y")
            due_date = input("What's the due date? Format your date like '01 Jan 1970': ")
            task_complete = "No"
            
            # Creating task string to append to tasks.txt file
            new_task = "\n" + assignee + ", " + task_title.strip() + ", " + task_description.strip() + \
                ", " + str(assignment_date) + ", " + due_date.strip() + ", " + task_complete.strip()

            # Opening tasks.txt and writing new task to it
            with open('tasks.txt', 'a') as task_file:
                task_file.write(new_task)
            break
        else:
            print("Invalid user entered! Please try again.")
            continue # Continuing 'while' loop if select_user does not exist in user.txt
def display_tasks(task_list):
    """
    This function takes any task list as an argument then prints out each task from the list
    in a more readable fashion.
    """

    for x, task in enumerate(task_list):

        print(dedent(f"""\
        {'-'*46} Task: {x+1} {'-'*46}
        Task:\t\t\t{task[1]}
        Assigned to:\t\t{task[0]}
        Date Assigned:\t\t{task[3]}
        Due Date:\t\t{task[4]}
        Task Complete?\t\t{task[5]}
        Task Description:\t{task[2]}
        """
            )
        )

def view_all():
    """
    This function users the read_tasks_from_file function to create a list of all
    tasks. It then passes this list to the display_task function which prints
    all the tasks in a more readable fashion.
    """

    print("\n", "*"*20, " TASK LIST (ALL) ", "*"*20, "\n")
    print("―"*100 + "\n")
    
    all_tasks = read_tasks_from_file() # creating list of tasks from txt file
    display_tasks(all_tasks) # displaying tasks using another function

def view_mine(current_user):
    """
    This function displays a list of tasks assigned to the logged in user.

    """
    
    all_tasks = read_tasks_from_file() # creating parent task list with all tasks
    my_tasks = [] # declaring a child list of the logged in user's tasks only

    while True:
        # extracting the user's tasks from the parent task list
        
        for x, task in enumerate(all_tasks):
            print(task[0])
            if task[0] == current_user:
                task.append(x) # x is the index of the task in the original tasks txt file for ref when editing tasks
                my_tasks.append(task) # adding task to user's task list
            else:
                continue

        if len(my_tasks) > 0: # Printing user's task list only if there are tasks assigned to the user
            print("―"*20 + f" TASKS FOR {current_user.upper()} " + "―"*20 + "\n")
            display_tasks(my_tasks)

            # Getting user's choice for task to be marked as complete or edited
            select_task = get_num("\nEnter the task number to open a task or enter (-1) to return to the main menu: ")
            if select_task != -1:
                edit_my_task(my_tasks, select_task) # Calling function for editing the selected task
            else:
                break   

        else: # This else block runs when there are no tasks assigned to the logged in user
            print("There are no tasks assigned to this user!")
            break
        
def read_tasks_from_file():
    """
    This function reads all tasks in the tasks txt file and returns them as a structured list
    """

    all_tasks = [] # Declaring a list where each task will be stored as one element
    task_info = [] # Declaing a list where a task will be stored with each detail as an element

    with open('tasks.txt', 'r') as task_file: # Opening task file in read-only mode
        content = task_file.readlines() # Extracting txt file contents 

        for line in content:
            task_info = line.strip().split(", ") # Splitting a task (line) into individual elements and storing in a list 
            all_tasks.append(task_info) # Appending task to all_tasks

    return all_tasks

def overwrite_file(filename, task_list):
    """
    This function overwrites a text file (first argument) with the contents of a list (second argument)
    """
    
    with open(str(filename), 'w') as file:
        for task in task_list:
            task_str = ", ".join(task) + "\n" # Creating a string from a list and adding new line character
            file.writelines(task_str) # writing task elements as a string to text file

def edit_my_task(task_list, task_num):
    """
    Takes a task list (child) and a selected task number as arguments, finds the index to the original task list (parent),
    then allows the user to mark the task as complete, or edit the assignee or due date. The changes are
    then overwritten to the tasks txt file.
    """
    
    while True:
        choice = get_num(dedent("""\
        Choose what you would like to do with the selected task.
        
        Enter 1 to mark task as complete
        Enter 2 to edit task
        Enter -1 to return to the previous menu
        
        Enter your choice here: """))

        all_tasks = read_tasks_from_file() # Getting list of tasks from tasks.txt file

        # Mark task as completed    
        if choice == 1:
            # Since the task list passed as an argument into this function is not the task list with all tasks,
            # the following code locates the selected task in the child list, then finds the index of that task
            # in the original all_tasks list (appended by another function), then applies changes to the parent
            # list.
            task_index_in_all_tasks = task_list[task_num-1][-1] # index to original transaction list is stored in last index
            all_tasks[task_index_in_all_tasks][-1] = "Yes"
            overwrite_file("tasks2.txt",all_tasks)

        # Change task assignee or due date
        elif choice == 2 and task_list[task_num-1][-2] == "No":
            user_or_date = get_num(dedent("""\
            \nChoose what you would like to change about this task.
        
            Enter 1 to change assignee
            Enter 2 to change due date
            Enter -1 to return to the previous menu
            
            Enter your choice here: """))

            # Change task assignee
            if user_or_date == 1:
                
                # getting user information from text file
                users = []
                with open('user.txt', 'r') as user_file:
                    content = user_file.readlines()

                    for line in content:
                        user, _ = line.strip().split(", ")
                        users.append(user)

                while True:
                    # Getting new assignee from user and checking if new assignee is registered
                    new_assignee = input("Who would you like this task assigned to? Enter username: ").lower()
                    if new_assignee not in users:
                        print("The user you entered is not registered. Please assign task to another user.")
                        continue
                    else:
                        # changing assignee
                        task_index_in_all_tasks = task_list[task_num-1][-1]
                        all_tasks[task_index_in_all_tasks][0] = "Yes"
                        overwrite_file("tasks2.txt",all_tasks) # writing changes to file using the overwrite function

            # Changing due date and checking if due date isn't past already
            if user_or_date == 2:
                current_due_date = datetime.strptime(task_list[task_num-1][4], "%d %b %Y").date() 
                date_today = datetime.now().date()

                if current_due_date > date_today:
                    print("True")
                    new_due_date = input("What's the due date? Format your date like '01 Jan 1970': ")
                    
                    # changing the due date
                    task_index_in_all_tasks = task_list[task_num-1][-1]
                    all_tasks[task_index_in_all_tasks][4] = new_due_date
                    overwrite_file("tasks2.txt", all_tasks)
                else:
                    print("This due date cannot be changed as it is already past")
        elif choice == 2 and task_list[task_num-1][-2] == "Yes":
            print("\nThis task cannot be edited as it has already been completed")
        elif choice == -1:
            break # Breaks the loop and returns to previous menu
        else:
            print("Invalid selection! Please enter a valid option.")     

def generate_user_report():
    """
    This function calculates some user metrics, generates a user overview report, and writes it to
    the user_overview.txt file.
    """
    
    all_tasks = read_tasks_from_file()
    users = [] # Declaring an empty list of users

    # Getting usernames from user.txt file
    with open('user.txt', 'r') as file:
        content = file.readlines()

        for line in content:
            user, _ = line.strip().split(', ')
            users.append(user)

    total_users = len(users) 
    total_tasks = generate_task_report() # generate_task_report returns total number of tasks

    # Calculating user metrics
    users_tasks_count = {} # Dictionary with users as keys and task counts as values
    users_incomplete_overdue_percentages = {} # Dictionary with users as keys and counts of incomplete
        # and overdue tasks as values

    users_completed_percentages = {} # Dictionary with users as keys and % of completed tasks as values
    users_incomplete_percentages = {} # Dictionary with users as keys and % of incomplete tasks as values

    today_date = datetime.now().date() # This will be used to check overdue tasks below
    for user in users:
        # The following counters will hold values for each user while the 'for' loop runs
        count_of_user_tasks = 0
        user_overdue_incomplete_count = 0
        user_completed_count = 0
        

        for task in all_tasks:
            # This loop goes through each task and increments the count_of_user_tasks, user_overdue_incomplete count,
            # and user_completed_count when a task is assigned to that user

            if task[0] == user:
                count_of_user_tasks += 1

            due_date = datetime.strptime(task[4], "%d %b %Y").date()
            if task[0] == user and task[-1] == "No" and due_date < today_date: # Checking for incomplete and overdue for user
                user_overdue_incomplete_count += 1

            if task[0] == user and task[-1] == "Yes": # checking for complete tasks for user
                user_completed_count += 1

        # To avoid ZeroDivisionError, count_of_user_tasks should always be greater than 0
        # This if block performs calculations on users with tasks assigned to them (count of tasks assigned > 0)    
        if count_of_user_tasks > 0:
            users_tasks_count[user] = int(count_of_user_tasks) # adding key/value pair of 'user':count_of_user_task' to related dict

            # Calculating and adding key/value pair of 'user':percentage_incomplete_overdue to related dict
            percentage_incomplete_overdue = round((user_overdue_incomplete_count / users_tasks_count[user]) * 100, 2)
            users_incomplete_overdue_percentages[user] = float(percentage_incomplete_overdue)

            # Calculating and adding key/value pairs of 'user':percentage_completed to related dict
            percentage_completed = round((user_completed_count / users_tasks_count[user]) * 100, 2)
            users_completed_percentages[user] = float(percentage_completed)

            # Calculating and adding key/value pairs of 'user':percentage_incomplete to related dict
            percentage_incomplete = round(((users_tasks_count[user] - user_completed_count) / users_tasks_count[user]) * 100, 2)
            users_incomplete_percentages[user] = float(percentage_incomplete)
        else: # Adding key/value pairs of 'user':0 to appropriate dicts where user has no tasks assigned to them
            users_tasks_count[user] = 0
            users_incomplete_overdue_percentages[user] = 0
            users_completed_percentages[user] = 0
            users_incomplete_percentages[user] = 0

    # Calculating percentage of total tasks assigned to each user

    users_tasks_percentage = {} # Dictionary with users as keys and % of total tasks assigned to users as values 
    
    for user in users_tasks_count:
        if users_tasks_count[user] > 0:
            percentage_of_total_tasks = round((users_tasks_count[user] / total_tasks) *100,2)
            users_tasks_percentage[user] = float(percentage_of_total_tasks)
        else:
             users_tasks_percentage[user] = 0
    
    user_overview_report = dedent(f"""\
    ---------------- USER OVERVIEW REPORT ---------------
    
    TASK AND USER OVERVIEW
    Total Number of Registered User : {total_users}
    Total Number of Tasks           : {total_tasks}
    """)

    with open('user_overview.txt', 'w') as file:
            file.write(user_overview_report)

    for user in users:

        per_user_report = dedent(f"""\
        ---------------------- {user.upper()} ----------------------
        
        Total Number of Tasks                       : {users_tasks_count.get(user)}
        Percentage of Tasks Allocated               : {users_tasks_percentage.get(user)}%
        Completion Progress                         : {users_completed_percentages.get(user)}% 
        Percentage of Tasks Incomplete              : {users_incomplete_percentages.get(user)}%
        Percentage of Tasks Overdue & Incomplete    : {users_incomplete_overdue_percentages.get(user)}%

        """)
        # Write reports to file
        with open('user_overview.txt', 'a') as file:
            file.write(per_user_report + "\n")
def extract_report(filename):
    """
    This function reads a report from a text file and prints it in the terminal
    """
    
    with open(filename, 'r') as file:
        content = file.readlines()

        for line in content:
            text = line.strip()
            print(text)

def generate_task_report():
    """
    This function generates a report of tasks and writes the report to the task_overview.txt file.
    The function is also used to calculate the total number of tasks which the function returns
    when called elsewhere in the program
    """
    
    all_tasks = read_tasks_from_file()

    # Calculation total number of tasks
    total_number_of_tasks = 0
    for task in all_tasks:
        if len(task) > 2:
            total_number_of_tasks += 1

    # Calculation completed tasks
    completed_tasks_count = 0
    for task in all_tasks:
        if task[-1] == "Yes":
            completed_tasks_count += 1
    
    # Calculation of incomplete tasks
    incomplete_tasks_count = len(all_tasks) - completed_tasks_count

    # Calculating count of incomplete and overdue tasks
    overdue_incomplete = 0
    for task in all_tasks:
        due_date = datetime.strptime(task[4], "%d %b %Y").date()
        today_date = datetime.now().date()
        task_completion = task[-1]

        if due_date < today_date and task_completion == "No":
            overdue_incomplete += 1

    # Percentage of tasks that are incomplete
    incomplete_percent = round((incomplete_tasks_count / total_number_of_tasks) * 100, )
    overdue_percentage = round(((total_number_of_tasks - completed_tasks_count) / total_number_of_tasks) * 100, 2)

    task_report = f"""---------------------- TASK OVERVIEW ----------------------
    
    Total Number of Tasks                       : {total_number_of_tasks}
    Total Number of Completed Tasks             : {completed_tasks_count}
    Total Number of Incompleted Tasks           : {incomplete_tasks_count}
    Total Count of Overdue and Incomplete Tasks : {overdue_incomplete}

    Percentage of Tasks that are Incomplete     : {incomplete_percent}
    Percentage of Tasks that are Overdue        : {overdue_percentage}"""

    # Write reports to file
    with open('task_overview.txt', 'w') as file:
        file.write(task_report)

    return total_number_of_tasks


print("\n", "*"*17, " WELCOME TO THE TASK MANAGER ", "*"*17)

#====Login Section====

username = "" # Storing username of logged in user for use in other menus

while True:
    # Presenting the login screen to user
    # Taking username and password input
    # Finding username and corresponding password in user.txt file

    print("\n", "―"*20, " LOGIN TO YOUR ACCOUNT ", "―"*20, "\n")
    username = input("Enter your username: ").lower()
    password = input("Enter your password: ")

    # usernames and matching passwords will be stored in the following
    # lists with corresponding entries having similar indexes
    users = []
    passwords = []
    
    # Opening user.txt and storing contents in a list called 'credentials'
    with open('user.txt', 'r') as login_file: 
        credentials = login_file.readlines() 

        for line in credentials:
            user, pwd = line.strip().split(", ")
            users.append(user.lower()) # Adding usernames to users list
            passwords.append(pwd) # Adding passwords to passwords list
    
    # Checking if 'username' value is in users list and if the 'password'
    # is equal to a member of passwords list in the same index as
    # username in users list.
    if username in users and password == passwords[users.index(username)]:
            print("\nLogin Successful!")
            break
    else:
        print("\nWrong password! Try again.\n")
        continue

while True:
    # presenting the menu to the user and 
    # username already converted to lower case at input

    if username == "admin":
        menu = input('''\nSelect one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - view my task
gr - generate reports
ds - display statistics
e - Exit
: ''').lower()
    else:
        menu = input('''\nSelect one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - view my task
e - Exit
: ''').lower()


    # ====Registering a new user as admin====
    if menu == 'r':
        reg_user(username)

    # ====Adding new task to tasks.txt====
    elif menu == 'a':                   
        add_task()
    # ====Displaying all tasks in tasks.txt===
    elif menu == 'va':
        view_all()

    # ====View tasks assigned to logged in user====
    elif menu == 'vm':
        view_mine(username)
    
    elif menu == 'gr' and username == 'admin':
        # Calling functions to generate reports and write them to file without displaying them
        generate_task_report()
        generate_user_report()
        print("Reports have been generated. Please check the ask and user overview text files.")

    # ====Displaying user and task count (admin only)====
    elif menu == 'ds' and username == 'admin':

        # Calling functions to generate and extract reports
        generate_task_report()
        generate_user_report()
        extract_report('task_overview.txt')
        print()
        extract_report('user_overview.txt')
    
    # ====Exiting the program====
    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again.")