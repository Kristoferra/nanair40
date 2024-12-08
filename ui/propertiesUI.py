from baseClasses.Property import Property
from logic.logicWrapper import Logic_Wrapper
from ui.searchUI import SearchUI
from ui.validationUI import ValidationUI


validation = ValidationUI()
AVAILABLE_EDIT_OPTIONS_FUNCTIONS = {'location': validation.validateText, 'address': validation.validateText, 'condition': validation.validateCondition, 'Facilities requiring maintenance': validation.validateText}
quitOrBack = ['q', 'b']


class PropertiesUI(SearchUI):
    def __init__(self, logicWrapper: Logic_Wrapper):
        self.logicWrapper = logicWrapper
    
    def addProperty(self) -> str:
        '''A new property is registered, user is asked various information about the new property'''

        # property dict keeps track of all the new items that the user has entered
        PropertyDict = {'Property number': '', 'location': '', 'address': '', 'condition': '', 'Facilities requiring maintnenance': '', 'rooms': '', 'facilities': ''}

        fields = [
            ('location', "Enter the location of the property: ", validation.validateText),
            ('address', "Enter the address of the property: ", validation.validateText),
            ('condition', "Condition(Excellent, Good, Fair, Poor): ", validation.validateCondition),
            ('Facilities requiring maintnenance', "Facilities requiring maintenance: ", validation.validateText),
        ]

        # property number needs to be a unique identifier so for each propertynumber the user enters, that property number is sent down to logic layer and checks if that propery number is already assigned to an employee in the system
        userPropertyNumber = None 
        while not userPropertyNumber: # While loop continues until a property number that is unique to the system is entered
            userPropertyNumber = self.getValidInput('Add property', "Enter a property number: ", validation.validateText, PropertyDict)
            if userPropertyNumber.lower() in quitOrBack:
                return userPropertyNumber.lower()
            
            # ask the logic layer whether this property is already in user, None is returned if it is 
            if self.logicWrapper.listProperties(id = userPropertyNumber): 
                userPropertyNumber = None # if the user entered a property number already in user then the while loops resets and the user is asked again
                continue
            PropertyDict['Property number'] = userPropertyNumber

        
        for key, prompt, validationFunc in fields: # This loops for all keys, prompts and functions the user needs to be askes
            value = self.getValidInput('Add property',prompt, validationFunc, PropertyDict)
            if value.lower() in quitOrBack: # If the user entered q or b, then we go back one page or quit
                return value.lower()
            PropertyDict[key] = value # the new valid value that the user entered is now set as the value to the key


        roomCount = self.getValidInput('Add property', 'How many rooms?: ', validation.validateNumber, PropertyDict) # Print menu and ask the user how many rooms there are in the property
        PropertyDict['rooms'] = roomCount
        idRoomDict = {}
        for i in range(int(roomCount)): # For loop continues for every room in the property
            userId = ''
            while userId not in idRoomDict: # WHILE LOOOP continues until a id that is not in the dict is entered
                room = f'room {i + 1}' 
                userId = self.getValidInput('Add property', f'Enter a id for room {i + 1}: ', validation.validateText, PropertyDict) # Ask the user for a room identifier for room number i
                if userId.lower() in quitOrBack: # if the user enters q or b then we quit or back
                    return userId
                
                if userId in idRoomDict: # if the user entered a key that was already in the dict then we reset the id and restart the while loop
                    userId = ''
                    continue
                idRoomDict[userId] = room # if the user entered a unique identifier then that is set as the key to room 'i'

        facilityçount = self.getValidInput('Add property', 'How many facilities?: ', validation.validateNumber,PropertyDict) # Ask the user how many special facilities there are in the system
        PropertyDict['facilities'] = facilityçount
        idFacilityDict = {}
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
        while not property: 
            # ask the user for a property numnber to look up
            lookUpproperty = self.getValidInput("Edit property","Enter property number: ", validation.validateText)
            if lookUpproperty.lower() in quitOrBack:
                return lookUpproperty.lower() # if the user enter to either quit or go back, we return that
            # ask the logic layer for the property number user entered, None is returned if the property number doesnt exist
            property = self.logicWrapper.listProperties(id = lookUpproperty) 

        # property items dict keeps track of the current values of the property the user entered
        properyItemsDict = {'location': property[0].location, 'address': property[0].address, 'condition': property[0].condition, 'facilities requiring maintenance': property[0].facilitiesMaintenance}
        valueToChange = ''
        while valueToChange not in properyItemsDict: # ask the user what he wants to change until he enters a value that is in the dictionary
            valueToChange = self.takeInputAndPrintMenu('', ('Edit employee', [f'{key}: {value}' for key, value in properyItemsDict.items()], 'Choose a value to change'))

        # ask the user for a new value based on what he chose to change, the new value is validated in the getvalidinput function
        newValue = self.getValidInput('Edit employee',f"Enter a new value for {valueToChange} {'(Excellent, Good, Fair, Poor)' if valueToChange.lower() == 'condition' else ''}", AVAILABLE_EDIT_OPTIONS_FUNCTIONS[valueToChange], properyItemsDict)
        properyItemsDict[valueToChange.lower()] = newValue # new value added to the properyItemsDict

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
        return self.takeInputAndPrintMenu('', ('Edit employee', [f'{key}: {value}' for key, value in properyItemsDict.items()], 'Property information has been succesfully updated\nChoose a option: '))

        


    def listProperties(self):
        '''lists all properies in the system in a table'''
        propertiesList = self.logicWrapper.listProperties() # get a list of instances, that include all properties in the system
        return self.showPropertyInfo(propertiesList) # call the showPropertyInfo functino in the searchUI class to print a table of all properties
        
        