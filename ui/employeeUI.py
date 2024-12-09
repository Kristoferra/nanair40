from ui.baseUI import BaseUI
from ui.validationUI import ValidationUI
from baseClasses.Employee import Employee
from logic.logicWrapper import Logic_Wrapper
from ui.searchUI import SearchUI
validation = ValidationUI() 

AVAILABLE_EDIT_OPTIONS_FUNCTIONS = {'name': validation.validateName, 'phone:': validation.validatePhone, 'homephone': validation.validatePhone, 'address': validation.validateText , 'email':  validation.validateEmail, 'location': validation.validateText}
quitOrBack = ['q', 'b']

class EmployeeUI(SearchUI):
    def __init__(self, logicWrapper: Logic_Wrapper):
        self.logicWrapper = logicWrapper # initialize the logic wrapper

    def addEmployee(self) -> str: # use employee base class
        '''A new employee is created and sent to the json file that stores all employees'''
        userClass = Employee()

        fields = [
 # These are all of the keys, prompts, and values that we need to ask the user
            ('name', "Enter your name: ", validation.validateName),
            ('phone', "Enter a phonenumber: ", validation.validatePhone),
            ('homePhone', "Enter a homephone: ", validation.validatePhone),
            ('address', "Enter a country: ", validation.validateText),
            ('email', "Enter your email: ", validation.validateEmail),
            ('location', "Enter your address: ", validation.validateText),
        ]

# Ask the user for a kennitala until he enters a unique kennitala or quits or backs
        employeeKennitala = None # kennitala needs to be a unique identifier so for each kennitala the user enters, that kennitala is sent down to logic layer and checks if that kennitala is already assigned to an employee in the system
        while not employeeKennitala: # While loop continues until a kennitala that is unique to the system is entered
            employeeKennitala = self.getValidInput('kennitala', "Enter a kennitala: ", validation.validateKennitala, userClass.__dict__)
            if employeeKennitala.lower() in quitOrBack: # if the user entered to quit or back then we return that
                return employeeKennitala.lower()
            if self.logicWrapper.listEmployees(kennitala = employeeKennitala): # pass the kennitala to the logic layer to check if its already in use
                employeeKennitala = None # if the kennitala is already in use then the while loop resets
                continue
            userClass.__dict__['kennitala'] = employeeKennitala # a unique kennital was entered and assigned to the new employee


        for key, prompt, validationFunc in fields: # This loops for all keys, prompts and functions the user needs to be askes
            value = self.getValidInput('Add employee',prompt, validationFunc, userClass.__dict__)
            if value.lower() in ('q', 'b'): # If the user entered q or b, then we go back one page or quit
                if value.lower() in quitOrBack:
                    return value.lower()
            userClass.__dict__[key] = value # add the key value pair to the instance


        # Here a instance would get created in order to send to data layer
        new_employee = Employee(userClass.__dict__['kennitala'], userClass.__dict__['name'], userClass.__dict__['phone'], userClass.__dict__['homePhone'], userClass.__dict__['location'], userClass.__dict__['email'], userClass.__dict__['address'])

        self.logicWrapper.addEmployee(new_employee) # ask the logic wrapper to create the new employee the user entered

        # User can then only choose from two options either quit or back
        return self.takeInputAndPrintMenu(['[Q]uit', '[B]ack'], ('Add employee', [f'{key}: {value if value else ''}' for key, value in userClass.__dict__.items()], 'The employee has been succesfully created\nChoose a option: ')) #



    def showEmployee(self) -> str:
        '''Asks the user to search for an employee, lists all information related to the employee and allows the user to edit some information about the employee searched for'''
        employee = None
        while not employee: # whilee loop keeps going until the wrapper sends a instance to the list
            lookUpKennitala = self.getValidInput("look for employee","Enter ID: ", validation.validateKennitala) # asks the user for a kennital until he enters a valid kennitala, or presses back/quit
            if lookUpKennitala.lower() in quitOrBack: # if the user entered to quit or go back we return that
                return lookUpKennitala.lower()
            
            employee = self.logicWrapper.listEmployees(kennitala=lookUpKennitala)  # Call the wrapper and check if a employee exists with the kennitala the user entered

        employee_list = [f'{key}: {value}' for key, value in list(employee[0].__dict__.items())[1:]] # create a list of key, value pairs from the employee the user asked for, we skip the first iteration that is kennitala

        userInput = ''

        while userInput not in AVAILABLE_EDIT_OPTIONS_FUNCTIONS: # here we allow the user to choose what he wants to change, the option he enters needs to be in the global dictionary that stores all options and their validation funcition
            self.printBaseMenu('look for employee', employee_list, 'Enter the value of what you would like to change: ')
            userInput = input(' ').lower()
            if userInput.lower() in quitOrBack: # if the user entered to quit or go back we return that
                return userInput.lower()
        # ask the user for a new value, the getvalidinput function asks for a new value and validates the value
        newValue = self.getValidInput('look for employee',  'Enter the new value: ', AVAILABLE_EDIT_OPTIONS_FUNCTIONS[userInput], employee[0].__dict__)
        if newValue.lower() in quitOrBack: # if the user entered to quit or go back we return that
            return newValue.lower()


        match userInput.lower(): # Matches what the user wanted to change, calls the logic wrapper function edit employee and changes the old value with the new one
            case 'name':
                self.logicWrapper.editEmployee(entry='kennitala', entryValue=lookUpKennitala, name = newValue)
            case 'phone':
                self.logicWrapper.editEmployee(entry='kennitala', entryValue=lookUpKennitala, phone = newValue)
            case 'homephone':
                self.logicWrapper.editEmployee(entry='kennitala', entryValue=lookUpKennitala, homePhone = newValue)
            case 'address':
                self.logicWrapper.editEmployee(entry='kennitala', entryValue=lookUpKennitala, address = newValue)
            case 'email':
                self.logicWrapper.editEmployee(entry='kennitala', entryValue=lookUpKennitala, email = newValue)
            case 'location':
                self.logicWrapper.editEmployee(entry='kennitala', entryValue=lookUpKennitala, location = newValue)
        
        employee = self.logicWrapper.listEmployees(kennitala = lookUpKennitala) # get the same employee from the json file with the upadted infromation
        # print the a menu with the updated employee information, and asking the user whether he wants to quit or go back
        return self.takeInputAndPrintMenu(['[Q]uit', '[B]ack'], ('List employees', [f'{key}: {value}' for key, value in list(employee[0].__dict__.items())], 'Employee information has been succesfuly updated!\nChoose a option: '))



    def showEmployees(self) -> str:
            '''prints a table of all employees in the system, after printing the user is asked whether he wants to quit or go back'''
            employeesList = self.logicWrapper.listEmployees()
            return self.showEmployeesInfo(employeesList)