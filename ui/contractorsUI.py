from baseClasses.Contractor import Contractor
from logic.logicWrapper import Logic_Wrapper
from ui.validationUI import ValidationUI
from ui.searchUI import SearchUI

validation = ValidationUI()
AVAILABLE_EDIT_OPTIONS_FUNCTIONS = {'name': validation.validateName, 'phone': validation.validatePhone, 'opening hours': validation.validateText, 'location': validation.validateText}
quitOrBack = ['q', 'b']

class ContractorsUI(SearchUI):
    def __init__(self, logicWrapper: Logic_Wrapper):
        self.logicWrapper = logicWrapper
    
    def showContractor(self):
        '''Asks the user whether he wants to list all contractors, add contractors or edit contractors info'''
        userInput = self.takeInputAndPrintMenu(['Add contractor', 'Edit contractor', 'List contractors'], ('Contractor Menu', ['Add contractor', 'Edit contractor', 'List contractors'], 'Choose a option'))

        match userInput.lower():
            case 'l':
                return self.showContractorsInfo()
            case 'a':
                return self.addContractor()
            case 'e':
                return self.editContractor()
            
        return userInput # if the user didnt enter any of the available options then he either quits or goes back
            
    def addContractor(self):
        contractorClass = Contractor()
        fields = [    # These are all of the keys, prompts, and values that we need to ask the user
            ('name', "Enter the name of the contractor: ", validation.validateName),
            ('phone', "Enter the phone number (Has to be 7 numbers long): ", validation.validatePhone),
            ('openingHours', "Write the opening hours(OPENING-CLOSING): ", validation.validateText),
        ]
        
        for key, prompt, validationFunc in fields: # This loops for all keys, prompts and functions the user needs to be askes
            value = self.getValidInput('Add contractor',prompt, validationFunc, contractorClass.__dict__)
            if value.lower() in quitOrBack: # If the user entered q or b, then we go back one page or quit
                return value.lower()
            contractorClass.__dict__[key] = value

        location = None
        destinations = self.logicWrapper.listLocations()
        employeeLocation =  self.takeInputAndPrintMenuWithoutBrackets('', ('Add property', [destination.airport for destination in destinations], 'choose a location')).capitalize()
        while not location:
            location = self.logicWrapper.listLocations(airport = employeeLocation)
            if not location:
                employeeLocation =  self.takeInputAndPrintMenuWithoutBrackets('', ('Add property', [destination.airport for destination in destinations], 'Please choose a location from the given options\nchoose a location: ')).capitalize()
        contractorClass.__dict__['location'] = employeeLocation



        
        # contractor isntance is created
        newContractor = Contractor(self.logicWrapper.currentContractorID, contractorClass.__dict__["name"], contractorClass.__dict__["phone"], contractorClass.__dict__["openingHours"], contractorClass.__dict__["location"])

        # contractor instance sent to the logic layer where its then stored in a json file
        self.logicWrapper.addContractor(newContractor)

        # Print a menu with all of the contractor information that was just created, the user can either quit or go back
        return self.takeInputAndPrintMenuWithoutBrackets(['[Q]uit', '[B]ack'], ('Add Constractor', [f'{key}: {value}' for key, value in newContractor.__dict__.items()], 'The Contractor has been succesfully created\nChoose a option: '))
        



    def editContractor(self):
        contractor = []
        while not contractor: # whilee loop keeps going until the wrapper sends a instance to the list
            lookUpContractor = self.showContractorsInfo('Enter contractor ID to edit: ', '')
            if lookUpContractor.lower() in quitOrBack:
                return lookUpContractor.lower()
            contractor = self.logicWrapper.listContractors(id=lookUpContractor)  # Call the wrapper and check if a employee exists with the kennitala the user entered

        # all of the current information about the contractor the user searched for is stores in contractorDict
        contractorDict = {'name': contractor[0].name, 'phone': contractor[0].phone, 'opening hours': contractor[0].openingHours, 'location': contractor[0].location}

        valueToChange = ''
        # user is asked for a value to change until he enters a value that is in the AVAILABLE_EDIT_OPTIONS_FUNCTIONS global variable
        while valueToChange not in AVAILABLE_EDIT_OPTIONS_FUNCTIONS: 
            # user asked for a value to change
            valueToChange = self.getValidInput('Edit contractor', 'Enter the value of what you would like to change: ', validation.validateText, contractorDict)

            if valueToChange.lower() in quitOrBack: # if the user entered to quit or go back
                return valueToChange.lower()
        if valueToChange == 'location':
            location = None
            destinations = self.logicWrapper.listLocations()
            employeeLocation =  self.takeInputAndPrintMenuWithoutBrackets('', ('Add property', [destination.airport for destination in destinations], 'choose a location')).capitalize()
            while not location:
                if employeeLocation.lower() in quitOrBack:
                    return employeeLocation.lower()
                location = self.logicWrapper.listLocations(airport = employeeLocation)
                if not location:
                    employeeLocation =  self.takeInputAndPrintMenuWithoutBrackets('', ('Add property', [destination.airport for destination in destinations], 'Please choose a location from the given options\nchoose a location: ')).capitalize()
            contractorDict['location'] = employeeLocation
            newValue = employeeLocation
        else:
            newValue = self.getValidInput('Edit contractor',  'Enter the new value: ', AVAILABLE_EDIT_OPTIONS_FUNCTIONS[valueToChange.lower()], contractorDict)

        # new value added to the dictionary that is keeping track of the contractors values
        contractorDict[valueToChange.lower()] = newValue

        # match what the user wants to change, the logic wrapper is called where he changes the value in the employee json file
        match valueToChange.lower(): 
            case 'name':
                self.logicWrapper.editContractor(entry= 'id', entryValue=lookUpContractor, name = newValue)
            case 'phone':
                self.logicWrapper.editContractor(entry='id', entryValue=lookUpContractor, phone = newValue)
            case 'opening hours':
                self.logicWrapper.editContractor(entry='id', entryValue=lookUpContractor, openingHours = newValue)
            case 'location':
                self.logicWrapper.editContractor(entry='id', entryValue=lookUpContractor, location = newValue)

        return self.takeInputAndPrintMenuWithoutBrackets(['[Q]uit', '[B]ack'], ('List employees', [f'{key}: {value}' for key, value in list(contractorDict.items())], 'Employee information has been succesfuly updated!\nChoose a option: '))



        
