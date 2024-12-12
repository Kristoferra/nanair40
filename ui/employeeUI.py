from ui.baseUI import BaseUI
from ui.validationUI import ValidationUI
from baseClasses.Employee import Employee
from logic.logicWrapper import Logic_Wrapper
from ui.searchUI import SearchUI
validation = ValidationUI() 

AVAILABLE_EDIT_OPTIONS_FUNCTIONS = {'name': validation.validateName, 'phone': validation.validatePhone, 'homephone': validation.validatePhone, 'address': validation.validateText , 'email':  validation.validateEmail, 'location': validation.validateText}
quitOrBack = ['q', 'b']

class EmployeeUI(SearchUI):
    def __init__(self, logicWrapper: Logic_Wrapper):
        self.logicWrapper = logicWrapper # initialize the logic wrapper

    def addEmployee(self) -> str: # use employee base class
        '''A new employee is created and sent to the json file that stores all employees'''
        userClass = Employee()

        fields = [
 # These are all of the keys, prompts, and values that we need to ask the user
            ('name', "Enter your name: ", validation.validateName, 'Invalid input\n'),
            ('phone', "Enter a phone number: ", validation.validatePhone, 'Phone number length has to be between 7-15\n'),
            ('homePhone', "Enter a homephone: ", validation.validatePhone, 'Phone number length has to be between 7-15\n'),
            ('address', "Enter a address: ", validation.validateText, 'Invalid input\n'),
            ('email', "Enter your email: ", validation.validateEmail, 'Email must include a "@" symbol\n'),
        ]

# Ask the user for a kennitala until he enters a unique kennitala or quits or backs
        employeeKennitala = None # kennitala needs to be a unique identifier so for each kennitala the user enters, that kennitala is sent down to logic layer and checks if that kennitala is already assigned to an employee in the system
        lookUpKennitala = self.getValidInput('kennitala', "Enter a kennitala: ", validation.validateKennitala, userClass.__dict__, 'Kennitala has to be 10 letters long!\n')
        while not employeeKennitala: # While loop continues until a kennitala that is unique to the system is entered
            if lookUpKennitala.lower() in quitOrBack: # if the user entered to quit or back then we return that
                return lookUpKennitala.lower()
            if self.logicWrapper.listEmployees(kennitala = lookUpKennitala): # pass the kennitala to the logic layer to check if its already in use
                lookUpKennitala = self.getValidInput('kennitala', "A employee already exists with that kennitala!\nEnter a kennitala: ", validation.validateKennitala, userClass.__dict__, 'Kennitala has to be 10 letters long!\n')
                employeeKennitala = None # if the kennitala is already in use then the while loop resets
                continue
            employeeKennitala = lookUpKennitala
            userClass.__dict__['kennitala'] = employeeKennitala # a unique kennital was entered and assigned to the new employee


        for key, prompt, validationFunc, errorMessage in fields: # This loops for all keys, prompts and functions the user needs to be askes
            value = self.getValidInput('Add employee',prompt, validationFunc, userClass.__dict__, errorMessage)
            if value.lower() in ('q', 'b'): # If the user entered q or b, then we go back one page or quit
                if value.lower() in quitOrBack:
                    return value.lower()
            userClass.__dict__[key] = value # add the key value pair to the instance

        location = None
        destinations = self.logicWrapper.listLocations() # get all availavle destionations/locations
        # ask the user for a input for a location and print the menu
        employeeLocation =  self.takeInputAndPrintMenuWithoutBrackets('', ('Choose a location', [destination.airport for destination in destinations], 'choose a location')).capitalize()
        while not location:
            if employeeLocation.lower() in quitOrBack: # go back or quit
                return employeeLocation.lower() 
            # check if the location the user enterd is available, wrapper returns none if there is no location with this input
            location = self.logicWrapper.listLocations(airport = employeeLocation) 
            if not location:
                # if no location matches the user input the user is asked again and the same menu is printed
                employeeLocation =  self.takeInputAndPrintMenu('', ('Choose a location', [destination.airport for destination in destinations], 'Please choose a location from the given options\nchoose a location: ')).capitalize()
        userClass.__dict__['location'] = employeeLocation

        # Here a instance would get created in order to send to data layer
        new_employee = Employee(userClass.__dict__['kennitala'], userClass.__dict__['name'], userClass.__dict__['phone'], userClass.__dict__['homePhone'], userClass.__dict__['address'], userClass.__dict__['email'], userClass.__dict__['location'])

        # new employee instance sent down to logic layer where, and then stored in json file if all is valid
        self.logicWrapper.addEmployee(new_employee) # ask the logic wrapper to create the new employee the user entered

        # User can then only choose from two options either quit or back
        return self.takeInputAndPrintMenuWithoutBrackets(['[Q]uit', '[B]ack'], ('Add employee', [f'{key}: {value if value else ''}' for key, value in userClass.__dict__.items()], 'The employee has been succesfully created\nChoose a option: ')) #



    def showEmployee(self) -> str:
        '''Asks the user to search for an employee, lists all information related to the employee and allows the user to edit some information about the employee searched for'''
        employee = None
        lookUpKennitala = self.getValidInput("look for employee","Enter ID: ", validation.validateKennitala)
        while not employee: # whilee loop keeps going until the wrapper sends a instance to the list
            if lookUpKennitala.lower() in quitOrBack: # if the user entered to quit or go back we return that
                return lookUpKennitala.lower()
            employee = self.logicWrapper.listEmployees(kennitala=lookUpKennitala)  # Call the wrapper and check if a employee exists with the kennitala the user entered
            if not employee:
                lookUpKennitala = self.getValidInput("look for employee", "No employee in the system has this kennitala\nEnter ID: ", validation.validateKennitala)

        employee_list = [f'{key}: {value}' for key, value in list(employee[0].__dict__.items())[1:]] # create a list of key, value pairs from the employee the user asked for, we skip the first iteration that is kennitala

        valueToChange = ''

        while valueToChange.lower() not in AVAILABLE_EDIT_OPTIONS_FUNCTIONS: # here we allow the user to choose what he wants to change, the option he enters needs to be in the global dictionary that stores all options and their validation funcition
            valueToChange = self.takeInputAndPrintMenuWithoutBrackets('', ('look for employee', employee_list, 'Enter the value of what you would like to change: '))
            if valueToChange.lower() in quitOrBack: # if the user entered to quit or go back we return that
                return valueToChange.lower()
        # ask the user for a new value, the getvalidinput function asks for a new value and validates the value


        if valueToChange == 'location':
            location = None
            # get a list of all locations by calling the wrapper
            destinations = self.logicWrapper.listLocations()
            #ask the user for a new location change
            employeeLocation =  self.takeInputAndPrintMenuWithoutBrackets('', ('Choose a location', [destination.airport for destination in destinations], 'choose a location')).capitalize()
            while not location:
                if employeeLocation.lower() in quitOrBack: # quit or go back if the user asked for that
                    return employeeLocation.lower()
                # check with the locig wrappet whether the location user entered exists, if not None is returned
                location = self.logicWrapper.listLocations(airport = employeeLocation)
                if not location:
                    # if logic layer returned none, then the user is asked again
                    employeeLocation =  self.takeInputAndPrintMenuWithoutBrackets('', ('Choose a location', [destination.airport for destination in destinations], 'Please choose a location from the given options\nchoose a location: ')).capitalize()
            newValue = employeeLocation

        else:
            # if new value is not location, then the user is asked for a new to change, this value is then validated from the global dictionary
            newValue = self.getValidInput('look for employee',  'Enter the new value: ', AVAILABLE_EDIT_OPTIONS_FUNCTIONS[valueToChange], employee[0].__dict__)
            if newValue.lower() in quitOrBack: # if the user entered to quit or go back we return that
                return newValue.lower()


        match valueToChange.lower(): # Matches what the user wanted to change, calls the logic wrapper function edit employee and changes the old value with the new one
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
        return self.takeInputAndPrintMenuWithoutBrackets(['[Q]uit', '[B]ack'], ('List employees', [f'{key}: {value}' for key, value in list(employee[0].__dict__.items())], 'Employee information has been succesfuly updated!\nChoose a option: '))



    def showEmployees(self) -> str:
            '''prints a table of all employees in the system, after printing the user is asked whether he wants to quit or go back'''
            employeesList = self.logicWrapper.listEmployees()
            return self.showEmployeesInfo(employeesList)