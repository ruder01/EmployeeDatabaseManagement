import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import mysql.connector
from mysql.connector import Error

# Global variable to store employee data
employees_data = []

# Establish database connection
def connect(host, database, user, password):
    try:
        connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        if connection.is_connected():
            return connection
    except Error as e:
        messagebox.showerror("Error", f"Error connecting to MySQL database: {e}")
        return None

# Function to prompt user for database credentials
def get_db_credentials():
    host = simpledialog.askstring("Database Connection", "Enter the database host address:")
    database = simpledialog.askstring("Database Connection", "Enter the database name:")
    user = simpledialog.askstring("Database Connection", "Enter the username:")
    password = simpledialog.askstring("Database Connection", "Enter the password:", show="*")
    return host, database, user, password

# Fetch all employees from the Employees table
def fetch_employees():
    global employees_data
    employees_data = []  # Clear previous data
    try:
        connection = connect(host, database, user, password)
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT employee_id, first_name, last_name, email, phone, hire_date, salary, project_id FROM Employees")
            employees_data = cursor.fetchall()
    except Error as e:
        messagebox.showerror("Error", f"Error fetching employees: {e}")
    finally:
        if connection:
            connection.close()

# Populate the employee listbox
def populate_listbox():
    fetch_employees()
    listbox_employees.delete(0, tk.END)  # Clear previous items
    for employee in employees_data:
        full_name = f"{employee[1]} {employee[2]}"
        listbox_employees.insert(tk.END, full_name)


# Handle selection in the employee listbox
def on_select(event):

    selected_index = listbox_employees.curselection()
    if selected_index:
        selected_employee = employees_data[selected_index[0]]
        employee_id.set(selected_employee[0])
        first_name.set(selected_employee[1])
        last_name.set(selected_employee[2])
        email.set(selected_employee[3])
        phone.set(selected_employee[4])
        hire_date.set(selected_employee[5])
        salary.set(selected_employee[6])
        project_id.set(selected_employee[7])
        
        fetch_project_details()

def fetch_project_ids():
    try:
        connection = connect(host, database, user, password)
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT project_id FROM Projects")
            project_ids = [row[0] for row in cursor.fetchall()]
            return project_ids
    except Error as e:
        messagebox.showerror("Error", f"Error fetching project IDs: {e}")
    finally:
        if connection:
            connection.close()

# Add a new employee
def open_add_employee_window():
    add_employee_window = tk.Toplevel(root)
    add_employee_window.title("Add Employee")

    # Employee details labels and entry fields
    tk.Label(add_employee_window, text="First Name:").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(add_employee_window, text="Last Name:").grid(row=1, column=0, padx=5, pady=5)
    tk.Label(add_employee_window, text="Email:").grid(row=2, column=0, padx=5, pady=5)
    tk.Label(add_employee_window, text="Phone:").grid(row=3, column=0, padx=5, pady=5)
    tk.Label(add_employee_window, text="Hire Date (YYYY-MM-DD):").grid(row=4, column=0, padx=5, pady=5)
    tk.Label(add_employee_window, text="Salary:").grid(row=5, column=0, padx=5, pady=5)
    tk.Label(add_employee_window, text="Project ID:").grid(row=6, column=0, padx=5, pady=5)

    # Create separate StringVar objects for entry fields in the "Add Employee" window
    add_first_name = tk.StringVar()
    add_last_name = tk.StringVar()
    add_email = tk.StringVar()
    add_phone = tk.StringVar()
    add_hire_date = tk.StringVar()
    add_salary = tk.DoubleVar()
    add_project_id = tk.StringVar()


    first_name_entry = tk.Entry(add_employee_window, textvariable=add_first_name)
    last_name_entry = tk.Entry(add_employee_window, textvariable=add_last_name)
    email_entry = tk.Entry(add_employee_window, textvariable=add_email)
    phone_entry = tk.Entry(add_employee_window, textvariable=add_phone)
    hire_date_entry = tk.Entry(add_employee_window, textvariable=add_hire_date)
    salary_entry = tk.Entry(add_employee_window, textvariable=add_salary)
    project_combobox = ttk.Combobox(add_employee_window, textvariable=add_project_id, state="readonly")
    project_combobox.grid(row=6, column=1, padx=5, pady=5)

    project_ids = fetch_project_ids()
    if project_ids:
        project_combobox['values'] = project_ids


    first_name_entry.grid(row=0, column=1, padx=5, pady=5)
    last_name_entry.grid(row=1, column=1, padx=5, pady=5)
    email_entry.grid(row=2, column=1, padx=5, pady=5)
    phone_entry.grid(row=3, column=1, padx=5, pady=5)
    hire_date_entry.grid(row=4, column=1, padx=5, pady=5)
    salary_entry.grid(row=5, column=1, padx=5, pady=5)

    # Function to add a new employee
    def add_employee():
        first_name_value = add_first_name.get()
        last_name_value = add_last_name.get()
        email_value = add_email.get()
        phone_value = add_phone.get()
        hire_date_value = add_hire_date.get()
        salary_value = add_salary.get()
        project_id_value = add_project_id.get()

        try:
            connection = connect(host, database, user, password)
            if connection:
                cursor = connection.cursor()
                sql_query = """INSERT INTO Employees (first_name, last_name, email, phone, hire_date, salary, project_id)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                employee_data = (first_name_value, last_name_value, email_value, phone_value, hire_date_value, salary_value, project_id_value)
                cursor.execute(sql_query, employee_data)
                connection.commit()
                messagebox.showinfo("Success", "Employee added successfully")
                populate_listbox()  # Refresh listbox after adding
                add_employee_window.destroy()
        except Error as e:
            messagebox.showerror("Error", f"Error adding employee: {e}")
        finally:
            if connection:
                connection.close()
    
    # Button to add new employee
    tk.Button(add_employee_window, text="Add Employee", command=add_employee).grid(row=7, column=0, columnspan=2, padx=5, pady=10)


# Update the selected employee
def update_employee():
    employee_id_value = employee_id.get()
    first_name_value = first_name.get()
    last_name_value = last_name.get()
    email_value = email.get()
    phone_value = phone.get()
    hire_date_value = hire_date.get()
    salary_value = salary.get()
    project_id_value = project_id.get()

    try:
        connection = connect(host, database, user, password)
        if connection:
            cursor = connection.cursor()
            sql_query = """UPDATE Employees
                           SET first_name = %s, last_name = %s, email = %s, phone = %s, hire_date = %s, salary = %s, project_id = %s
                           WHERE employee_id = %s"""
            employee_data = (first_name_value, last_name_value, email_value, phone_value, hire_date_value, salary_value, project_id_value, employee_id_value)
            cursor.execute(sql_query, employee_data)
            connection.commit()
            messagebox.showinfo("Success", "Employee details updated successfully")
            populate_listbox()  # Refresh listbox after updating
    except Error as e:
        messagebox.showerror("Error", f"Error updating employee details: {e}")
    finally:
        if connection:
            connection.close()

# Delete the selected employee
def delete_employee():
    selected_index = listbox_employees.curselection()
    if selected_index:
        employee_id_value = employees_data[selected_index[0]][0]
        try:
            connection = connect(host, database, user, password)
            if connection:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM Employees WHERE employee_id = %s", (employee_id_value,))
                connection.commit()
                messagebox.showinfo("Success", "Employee deleted successfully")
                populate_listbox()  # Refresh listbox after deletion
        except Error as e:
            messagebox.showerror("Error", f"Error deleting employee: {e}")
        finally:
            if connection:
                connection.close()

# Create the main GUI window
root = tk.Tk()
root.title("Employee Database Management")

# Prompt user for database credentials
host, database, user, password = get_db_credentials()

# Employee listbox
label_employees = tk.Label(root, text="Employees", font=("Helvetica", 10))
label_employees.grid(row=0, column=0, sticky='ew', padx=10, pady=10)

listbox_employees = tk.Listbox(root, width=40, height=10)
listbox_employees.grid(row=1, column=0 ,padx=10, pady=10)
listbox_employees.bind("<<ListboxSelect>>", on_select)

# Fetch employees and populate the listbox
populate_listbox()

# Employee details frame on the right side
label_employees_details = tk.Label(root, text="Employees Details", font=("Helvetica", 10))
label_employees_details.grid(row=0, column=1, sticky='ew', padx=10, pady=10)
details_frame = ttk.Notebook(root)
details_frame.grid(row=1, column=1, padx=10, pady=10) 

# General tab
general_tab = ttk.Frame(details_frame)
details_frame.add(general_tab, text='General')


tk.Label(general_tab, text="Employee ID:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
employee_id = tk.StringVar()
tk.Label(general_tab, textvariable=employee_id).grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

tk.Label(general_tab, text="First Name:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
first_name = tk.StringVar()
first_name_entry = tk.Entry(general_tab, textvariable=first_name, state='normal')  # 'normal' state allows editing
first_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

tk.Label(general_tab, text="Last Name:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
last_name = tk.StringVar()
last_name_entry = tk.Entry(general_tab, textvariable=last_name, state='normal')
last_name_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

tk.Label(general_tab, text="Email:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
email = tk.StringVar()
email_entry = tk.Entry(general_tab, textvariable=email, state='normal')
email_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

tk.Label(general_tab, text="Phone:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
phone = tk.StringVar()
phone_entry = tk.Entry(general_tab, textvariable=phone, state='normal')
phone_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

tk.Label(general_tab, text="Hire Date (YYYY-MM-DD):").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
hire_date = tk.StringVar()
hire_date_entry = tk.Entry(general_tab, textvariable=hire_date, state='normal')
hire_date_entry.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)

tk.Label(general_tab, text="Salary:").grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
salary = tk.DoubleVar()
salary_entry = tk.Entry(general_tab, textvariable=salary, state='normal')
salary_entry.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)

project_id = tk.StringVar()


# Project tab
project_tab = ttk.Frame(details_frame)
details_frame.add(project_tab, text='Project')

# Function to fetch and display project details
def fetch_project_details(event=None):
    try:
        connection = connect(host, database, user, password)
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Projects WHERE project_id = %s", (project_id.get(),))
            project_details = cursor.fetchone()
            if project_details:
                project_name_label.config(text="Project Name: " + project_details[1])
                start_date_label.config(text="Start Date: " + str(project_details[2]))
                end_date_label.config(text="End Date: " + str(project_details[3]))
                budget_label.config(text="Budget: $" + str(project_details[4]))
            
            # Display project details (omitted for brevity)
            
    except Error as e:
        messagebox.showerror("Error", f"Error fetching project details: {e}")
    finally:
        if connection:
            connection.close()

tk.Label(project_tab, text="Project ID:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
project_ids = fetch_project_ids()
if project_ids:
    project_combobox = ttk.Combobox(project_tab, textvariable=project_id, values=project_ids, state="readonly")
    project_combobox.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
    project_combobox.bind("<<ComboboxSelected>>", fetch_project_details)
    fetch_project_details()
else:
    messagebox.showinfo("Info", "No project IDs found")

# Labels to display project details
project_name_label = tk.Label(project_tab, text="Project Name: ")
project_name_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

start_date_label = tk.Label(project_tab, text="Start Date: ")
start_date_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

end_date_label = tk.Label(project_tab, text="End Date: ")
end_date_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

budget_label = tk.Label(project_tab, text="Budget: ")
budget_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)

# Buttons to perform database operations
tk.Button(root, text="Add Employee", command=open_add_employee_window).grid(row=8, column=0, padx=5, pady=10)
tk.Button(root, text="Update Employee", command=update_employee).grid(row=8, column=1, padx=5, pady=10)
tk.Button(root, text="Delete Employee", command=delete_employee).grid(row=8, column=2, padx=5, pady=10)

# Run the main event loop
root.mainloop()
