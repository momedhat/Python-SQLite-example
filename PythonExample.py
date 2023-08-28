####### CREATING DATABASE AND MINABULATE DATA USING PYTHON (sqllite LIBRARY) #######

def exceptions_decorator(func):
    def wrapper(self, *param):
        try:
            func(self,*param)
            print("The method has run successfully...")
        except:
            print("There is an error occured!!")
    return wrapper

import sqlite3

class Employee:

    employee_list = [] # list of employee objects -- static list 

    db = sqlite3.connect("newdb.sqlite")
    curs = db.cursor()

    create_emp_table = "CREATE TABLE IF NOT EXISTS employee (first_name TEXT, \
                    last_name TEXT, \
                    age int, \
                    department TEXT, \
                    salary int)"


    #CONSTRUCTOR#
    def __init__(self, first_name='', last_name='', age=0, department='none', salary=0):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.department = department
        self.salary = salary
        
        Employee.curs.execute(Employee.create_emp_table) # Create Table on DB if not existed
        Employee.employee_list.append(self) # insert the obj into employee_list
        self.__insert_into_table() # insert new record in table employee in DB
        
        Employee.db.commit()

    @exceptions_decorator
    def __insert_into_table(self):
        insert_query = "INSERT INTO employee (first_name, last_name, age, department, salary) VALUES (?, ?, ?, ?, ?)"
        values = (self.first_name, self.last_name, self.age, self.department, self.salary)
        Employee.curs.execute(insert_query, values)
        
        Employee.db.commit()
            

    @exceptions_decorator
    def transfer(self, department): # update the department for the employee
        update_query = "UPDATE employee SET department = ? WHERE first_name = ? AND last_name = ?"
        Employee.curs.execute(update_query, (department, self.first_name, self.last_name))
        
        Employee.db.commit()

    
    @exceptions_decorator
    def fire(self): # delete employee from the table
        Employee.employee_list.remove(self)
        delete_emp_query = "DELETE FROM employee WHERE first_name = ? AND last_name = ?"
        Employee.curs.execute(delete_emp_query, (self.first_name, self.last_name))
        
        Employee.db.commit()

    
    def show(self): # Print the employee data 
        print(f"Employee name: {self.first_name } {self.last_name}")
        print(f"Employee age: {self.age}")
        print(f"Employee department: {self.department}")
        print(f"Employee salary: {self.salary}")

    @staticmethod
    def list_employee(): # Select all employees and print their data
        Employee.curs.execute("SELECT * FROM employee")
        employees = Employee.curs.fetchall()
        for emp in employees:
            print (emp)

        Employee.db.commit()





####Testing####

#Inset employee data
emp1 = Employee("Mohamed","Medhat",24,"Data Engineering", 1000)
emp2 = Employee("Ahmed","Mohamed",20,"Hr", 2000)
emp3 = Employee("Ali","Mohamed",20,"Finance", 2000)
emp4 = Employee() # with no parameters to get the default values


#Get employee data
emp1.show()

#List all employees
Employee.list_employee()

# Update department
emp3.transfer("Testing")

#Delete the employee data
emp4.fire()

#Re-check the table after edition
Employee.list_employee()
