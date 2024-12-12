from baseClasses.Property import Property
from logic.logicWrapper import Logic_Wrapper
from ui.searchUI import SearchUI
from ui.validationUI import ValidationUI


validation = ValidationUI()
AVAILABLE_EDIT_OPTIONS_FUNCTIONS = {'location': validation.validateText, 'address': validation.validateText, 'condition': validation.validateCondition, 'facilities maintenance': validation.validateText}
quitOrBack = ['q', 'b']


class PropertiesUI(SearchUI):
    def __init__(self, logicWrapper: Logic_Wrapper):
        self.logicWrapper = logicWrapper
    
    def addProperty(self) -> str:
        '''A new property is registered, user is asked various information about the new property'''

        # property dict keeps track of all the new items that the user has entered
        PropertyDict = {'Property number': '', 'location': '', 'address': '', 'condition': '', 'Facilities requiring maintnenance': '', 'rooms': '', 'facilities': ''}



        # property number needs to be a unique identifier so for each propertynumber the user enters, that property number is sent down to logic layer and checks if that propery number is already assigned to an employee in the system
        userPropertyNumber = None 
        lookUpPropertyNumber = self.getValidInput('Add property', "Enter a property number: ", validation.validateText, PropertyDict)
        while not userPropertyNumber: # While loop continues until a property number that is unique to the system is entered
            if lookUpPropertyNumber.lower() in quitOrBack:
                return lookUpPropertyNumber.lower()
            
            # ask the logic layer whether this property is already in user, None is returned if it is 
            if self.logicWrapper.listProperties(id = lookUpPropertyNumber): 
                lookUpPropertyNumber = self.getValidInput('Add property', "A property already exists with that property number!\nEnter a property number: ", validation.validateText, PropertyDict)
                userPropertyNumber = None # if the user entered a property number already in user then the while loops resets and the user is asked again
                continue
            userPropertyNumber = lookUpPropertyNumber
            PropertyDict['Property number'] = userPropertyNumber

        location = None
        #  call the logic layer to return a list of all location instances
        destinations = self.logicWrapper.listLocations()
        # ask the user what location he wants to assign the property, also prints menu with available locations
        employeeLocation =  self.takeInputAndPrintMenu('', ('Add property', [destination.airport for destination in destinations], 'choose a location')).capitalize()
        while not location:
            if employeeLocation.lower() in quitOrBack: # quit or go back
                return employeeLocation.lower()
            # call the logic wrapper to get a locations from the input the user entered, if location doesnt exist then none is returned
            location = self.logicWrapper.listLocations(airport = employeeLocation)
            if not location:
                # ask user again if invalid inputt
                employeeLocation =  self.takeInputAndPrintMenu('', ('Add property', [destination.airport for destination in destinations], 'Please choose a location from the given options\nchoose a location: ')).capitalize()
        PropertyDict['location'] = employeeLocation




        fields = [
            ('address', "Enter the address of the property: ", validation.validateText, 'Invalid address\n'),
            ('condition', "Condition(Excellent, Good, Fair, Poor): ", validation.validateCondition, 'Please choose from the options available\n'),
            ('Facilities requiring maintnenance', "Facilities requiring maintenance: ", validation.validateText, 'Invalid input'),
        ]

        for key, prompt, validationFunc, errorMessage in fields: # This loops for all keys, prompts and functions the user needs to be askes
            value = self.getValidInput('Add property',prompt, validationFunc, PropertyDict, errorMessage)
            if value.lower() in quitOrBack: # If the user entered q or b, then we go back one page or quit
                return value.lower()
            PropertyDict[key] = value # the new valid value that the user entered is now set as the value to the key


        roomCount = self.getValidInput('Add property', 'How many rooms?: ', validation.validateNumber, PropertyDict, 'Number has to be bigger than 0\n') # Print menu and ask the user how many rooms there are in the property
        PropertyDict['rooms'] = roomCount
        idRoomDict = {} # a dictionary that keeps track of the user input
        for i in range(int(roomCount)): # For loop continues asking the user for a room and id for the amount the user entered
            userId = ''
            while userId not in idRoomDict: # WHILE LOOP continues until a id that is not in the dict is entered
                room = f'room {i + 1}' 
                userId = self.getValidInput('Add property', f'Enter a id for room {i + 1}: ', validation.validateText, PropertyDict) # Ask the user for a room identifier for room number i
                if userId.lower() in quitOrBack: # if the user enters q or b then we quit or back
                    return userId.lower()
                
                if userId in idRoomDict: # if the user entered a key that was already in the dict then we reset the id and restart the while loop
                    userId = ''
                    continue
                idRoomDict[userId] = room # if the user entered a unique identifier then that is set as the key to room 'i'

        facilityçount = self.getValidInput('Add property', 'How many facilities?: ', validation.validateNumber,PropertyDict, 'Number has to be bigger than 0\n') # Ask the user how many special facilities there are in the system
        PropertyDict['facilities'] = facilityçount
        idFacilityDict = {} # dictionary that keeps track of user input
        for i in range(int(facilityçount)): # for loop continues while we go through each of the facilites needed
            userId = ''
            facility = self.getValidInput('Add property', 'Enter facility name?: ', validation.validateText, PropertyDict) # Ask the user what the name of the facility is
            while userId not in idFacilityDict: # while loop continues as long as the the id the user entered in is not in the dictionary
                if userId.lower() in quitOrBack:
                    return userId
                userId = self.getValidInput('Add property', f'Enter a id for {facility}: ', validation.validateText, PropertyDict)
                if userId.lower() in quitOrBack: # If the input is either b or q then we quit or back
                    return userId
                if userId in idFacilityDict: # if the id already exists in the dict then the the while loops resets
                    userId = ''
                    continue
                idFacilityDict[userId] = facility
        
        # create the property instance and send it to the wrapper where it is then stored in a json file
        propertyInstance = Property(PropertyDict['Property number'], PropertyDict['location'],  PropertyDict['address'], PropertyDict['condition'], PropertyDict['Facilities requiring maintnenance'], idRoomDict, idFacilityDict) 
        self.logicWrapper.addProperty(propertyInstance)

        # print the menu and give the option to either quit or go back
        return self.takeInputAndPrintMenu(['[Q]uit', '[B]ack'], ('Add Property', [f'{key}: {value}' for key, value in PropertyDict.items()], 'The Property has been succesfully created\nChoose a option: '))
        


    def showProperty(self) -> str:
        '''User searches for a property number and can edit information on that property number'''
        property = []
        # while loop continues asking the user for a property numner until he enters a proptery number that is in the system
        lookUpproperty = self.getValidInput("Edit property","Enter property number: ", validation.validateText)
        while not property: 
            # ask the user for a property numnber to look up
            if lookUpproperty.lower() in quitOrBack:
                return lookUpproperty.lower() # if the user enter to either quit or go back, we return that
            # ask the logic layer for the property number user entered, None is returned if the property number doesnt exist
            property = self.logicWrapper.listProperties(id = lookUpproperty)
            if not property:
                lookUpproperty = self.getValidInput("Edit property","A property property doesn´t exist with that property number\nEnter property number: ", validation.validateText)


        # property items dict keeps track of the current values of the property the user entered
        propertyItemsDict = {'location': property[0].location, 'address': property[0].address, 'condition': property[0].condition, 'facilities maintenance': property[0].facilitiesMaintenance}
        valueToChange = ''
        while valueToChange not in propertyItemsDict: # ask the user what he wants to change until he enters a value that is in the dictionary
            valueToChange = self.takeInputAndPrintMenu('', ('Edit property', [f'{key}: {value}' for key, value in propertyItemsDict.items()], 'Choose a value to change'))
            if valueToChange.lower() in quitOrBack:
                return valueToChange.lower()

        if valueToChange == 'location':
            location = None
            # call logic layer to get a list of all locations in the system
            destinations = self.logicWrapper.listLocations()
            # ask the user for a location while printing the options onto the screen
            employeeLocation =  self.takeInputAndPrintMenu('', ('Add property', [destination.airport for destination in destinations], 'choose a location')).capitalize()
            while not location:
                if employeeLocation.lower() in quitOrBack: 
                    return employeeLocation.lower()
                # check with logic layer if any location matches what the user entered, none is returned if nothing is found
                location = self.logicWrapper.listLocations(airport = employeeLocation)
                if not location:
                    # if no locations matches user input then user is asked again
                    location = None
                    employeeLocation =  self.takeInputAndPrintMenu('', ('Add property', [destination.airport for destination in destinations], 'Please choose a location from the given options\nchoose a location: ')).capitalize()
            propertyItemsDict['location'] = employeeLocation
            newValue = employeeLocation
        # ask the user for a new value based on what he chose to change, the new value is validated in the getvalidinput function
        else: 
            newValue = self.getValidInput('Edit employee',f"Enter a new value for {valueToChange} {'(Excellent, Good, Fair, Poor)' if valueToChange.lower() == 'condition' else ''}", AVAILABLE_EDIT_OPTIONS_FUNCTIONS[valueToChange], propertyItemsDict , '\nInvalid input')
            if newValue.lower() in quitOrBack:
                return newValue.lower()
            propertyItemsDict[valueToChange.lower()] = newValue # new value added to the properyItemsDict

        # matching what value the user chose to change, the logic wrapper is called and changes the old value with new in json file
        match valueToChange.lower(): 
            case 'location':
                self.logicWrapper.editProperty(entry='id', entryValue=lookUpproperty, location = newValue)
            case 'address':
                self.logicWrapper.editProperty(entry='id', entryValue=lookUpproperty, address = newValue)
            case 'facilities requiring maintenance':
                self.logicWrapper.editProperty(entry='id', entryValue=lookUpproperty, facilitiesMaintenance = newValue)
            case 'condition':
                self.logicWrapper.editProperty(entry='id', entryValue=lookUpproperty, condition = newValue)

        # print menu telling the user that the values have been changed, and he can either quit or go back
        return self.takeInputAndPrintMenu('', ('Edit employee', [f'{key}: {value}' for key, value in propertyItemsDict.items()], 'Property information has been succesfully updated\nChoose a option: '))

        


    def listProperties(self):
        '''lists all properies in the system in a table'''
        propertiesList = self.logicWrapper.listProperties() # get a list of instances, that include all properties in the system
        return self.showPropertyInfo(propertiesList) # call the showPropertyInfo functino in the searchUI class to print a table of all properties
        
        