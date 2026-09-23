import sqlite3

# Connect to the SQLite database.
connection = sqlite3.connect("company.db")

# Create a cursor to execute SQL statements.
cursor = connection.cursor()

# Create the tables.
cursor.execute("DROP TABLE IF EXISTS employee")
cursor.execute("DROP TABLE IF EXISTS department")

cursor.execute("""
    CREATE TABLE department (
        id INTEGER PRIMARY KEY,
        name TEXT,
        location TEXT
    )
""")

cursor.execute("""
    CREATE TABLE employee (
        id INTEGER PRIMARY KEY,
        name TEXT,
        deptid INTEGER
    )
""")

# Insert exactly five department records.
departments = [
    (1, "Human Resources", "Mumbai"),
    (2, "Finance", "Delhi"),
    (3, "Information Technology", "Bengaluru"),
    (4, "Sales", "Chennai"),
    (5, "Legal", "Hyderabad")
]

cursor.executemany(
    "INSERT INTO department (id, name, location) VALUES (?, ?, ?)",
    departments
)

# Insert exactly five employee records.
# DeptID 99 has no matching department.
# Department 5 has no employees assigned to it.
employees = [
    (1, "Aarav Sharma", 1),
    (2, "Priya Patel", 2),
    (3, "Rahul Verma", 3),
    (4, "Sneha Iyer", 4),
    (5, "Vikram Singh", 99)
]

cursor.executemany(
    "INSERT INTO employee (id, name, deptid) VALUES (?, ?, ?)",
    employees
)

# Save the changes.
connection.commit()

# Display all employees.
print("Employees:")
print("ID | Name           | DeptID")
print("-" * 32)

cursor.execute("SELECT id, name, deptid FROM employee")
for employee in cursor.fetchall():
    print(f"{employee[0]}  | {employee[1]:14} | {employee[2]}")

# Display all departments.
print("\nDepartments:")
print("ID | Name                 | Location")
print("-" * 40)

cursor.execute("SELECT id, name, location FROM department")
for department in cursor.fetchall():
    print(f"{department[0]}  | {department[1]:20} | {department[2]}")

# Display employees who work in Human Resources.
print("\nHR Employees:")
print("Name")
print("-" * 20)

cursor.execute("""
    SELECT employee.name
    FROM employee
    INNER JOIN department
        ON employee.deptid = department.id
    WHERE department.name = 'Human Resources'
""")

for employee in cursor.fetchall():
    print(employee[0])

# Close the cursor and database connection.
cursor.close()
connection.close()