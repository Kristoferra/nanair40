from logic.logicWrapper import Logic_Wrapper
from ui.baseUI import BaseUI
from ui.validationUI import ValidationUI
from ui.searchUI import SearchUI
from baseClasses.workOrder import WorkOrder

validation = ValidationUI()
AVAILABLE_EDIT_OPTIONS = ['description', 'property number', 'priority', 'contractor', 'room id']
quirOrBack = ['q', 'b']


class ManagerWorkOrder(SearchUI):
    def __init__(self, logicWrapper: Logic_Wrapper):
        self.logicWrapper = logicWrapper

    def addNewWorkOrder(self) -> str:
        ''' Creates a new work order by gathering user input for a description, property number, and room or facility ID, ensuring valid entries at each step. 'q' or 'b' is returned based on users options'''
        body = [] # body is user to keep track of what to print to the screen
        # ask the manager for a description of work order and printing menu
        Userdescription = self.takeInputAndPrintMenuWithoutBrackets('', ('Create work order', '', 'Description of work order: ')) # Get a description on what needs to be done
        if Userdescription in quirOrBack: # if user quits or goes 
            return Userdescription
        body.append(f'Work description: {Userdescription}')

        property = [] 
        lookUpPropertyNumber = self.takeInputAndPrintMenuWithoutBrackets('', ('Create work order', body, 'Enter a property number: ')) # Ask the user for a property number
        while not property: # While loops keeps going until the wrapper is able return a property instance, it only returns a instance when a correct property number is entered
            if lookUpPropertyNumber in quirOrBack:
                return lookUpPropertyNumber
            # ask the logic layer whether a property number exists with the user input, none is returned if it doesnt exist
            property = self.logicWrapper.listProperties(id = lookUpPropertyNumber) # Check whether a property exists with the number, if it does then a list of a single isntance is returned
            if not property:
            #ask the user again if not found
                lookUpPropertyNumber = self.takeInputAndPrintMenuWithoutBrackets('', ('Create work order', body, 'A property doesnt exist with that property number\nEnter a property number: ')) # Ask the user for a property number

        body.append(f'Property Number: {lookUpPropertyNumber}')

        managerRoomFacilityId = ''
        roomOrfacility = self.takeInputAndPrintMenuWithoutBrackets('', ('Create work order', body, 'Room or facility?: ')) # Ask the manager whether a facility or a room needs fixing
        while not managerRoomFacilityId: # While loop continues until enters a valid id for either room or facility
            if roomOrfacility.lower() in quirOrBack:
                return roomOrfacility.lower()
            
            # CHECKING if the user wants to see key value pairs for rooms or facilities
            match roomOrfacility.lower(): 
                case 'room':
                    idDict = property[0].rooms # if the manager chose a room then we use the room id dict
                case 'facility':
                    idDict = property[0].facilities # if the manager chose a facility then we use the facility dict
                case _:
                    roomOrfacility = self.takeInputAndPrintMenuWithoutBrackets('', ('Create work order', body, 'Please pick either room or facility\nRoom or facility?: ')) # Ask the manager whether a facility or a room needs fixing
                    continue
            # ask the user to choose from the available ids
            managerRoomFacilityId = self.takeInputAndPrintMenuWithoutBrackets('', ('Create work order', [f'{value}: {key}' for key, value in idDict.items()], 'Choose a ID: '))
            while managerRoomFacilityId not in idDict: # print a menu with all the id's the user can choose from, while loop continues until the user enters a id that matches a id in the dictionary
                managerRoomFacilityId = self.takeInputAndPrintMenuWithoutBrackets('', ('Create work order', [f'{value}: {key}' for key, value in idDict.items()], 'Please choose a valid ID from the options above\nChoose a ID: '))
                if managerRoomFacilityId in quirOrBack:
                    return managerRoomFacilityId
            

        body.append(f'Room/facility id: {managerRoomFacilityId}')
        

        priority = False
        # ask the user fora priority on the work order
        userPriority = self.takeInputAndPrintMenuWithoutBrackets('', ('Create work order', body, 'How important? (Emergency, now, as soon as possible): '))
        while not priority: # While loop continues until the user enters a valid priority description
            if userPriority in quirOrBack:
                return userPriority
            if validation.validatePriority(userPriority): # validare the priority
                priority = True
            else:
                # if user entered a invalid priority then he is asked again
                userPriority = self.takeInputAndPrintMenuWithoutBrackets('', ('Create work order', body, 'Please choose one of three available options\nHow important? (Emergency, now, as soon as possible): '))

        body.append(f'Priority: {userPriority}') 

        
        # PRINT menu and ask the user whether a contractor should be assinged to the work order
        isContractor = self.takeInputAndPrintMenuWithoutBrackets(['Y', 'N'], ('Create work order', body, 'Contractor? (Y/N): ')) # The manager either chooses yes that there is a contracor or no that there isnt
        if isContractor.lower() in quirOrBack:
            return isContractor.lower()
        lookUpContractor = -1
        if isContractor.lower() == 'y': # if there is a contractor then the following if statement applies
            contractor = []
            while not contractor: # While loop continues until a contractor is chosen that is within the system
                # prints al available contractors and the manager can choose from the available options
                lookUpContractor = self.showContractorsInfo('Choose a contractor ID: ', '')
                if lookUpContractor in quirOrBack:
                    return lookUpContractor
                # ask thelogic layer whether a contractor exists with the id entered, none is returned if not and while loop resets
                contractor = self.logicWrapper.listContractors(id = lookUpContractor)
            
            body.append(f'Contractor: {contractor[0].name}')


    
        # printing menu and asking whether task is recuring
        isRecuring = self.takeInputAndPrintMenuWithoutBrackets(["Y", "N"], ("Add work ordder", body, "IS this task recurring(Y/N): "))
        repeating = False
        repeatInterval = 0
        if isRecuring.lower() == "y":
            repeating = True 
        if repeating: # check the user input adn setting the repeat interval based on what the user chose
            repeatIntervalStr = self.takeInputAndPrintMenu(["D", "W", "M", "Y"], ("Create a work order", ["Daily", "Weekly", "Monthly", "Yearly"], "Choose option: "))
            match repeatIntervalStr.upper():
                case "D":
                    repeatInterval = 1
                case "W":
                    repeatInterval = 2
                case "M":
                    repeatInterval = 3
                case "Y":
                    repeatInterval = 4
                case _:
                    return repeatIntervalStr
        #crearing a work order instance that will be sent to logic layer
        workOrderInstance = WorkOrder(id=self.logicWrapper.currentWorkOrderID, description=Userdescription, propertyNumber=lookUpPropertyNumber, priority = userPriority, contractorID=int(lookUpContractor), roomFacilityId= managerRoomFacilityId, repeating=repeating, repeatInterval=repeatInterval)
        self.logicWrapper.addWorkOrder(workOrderInstance)
       

        return self.takeInputAndPrintMenuWithoutBrackets(['[Q]uit', '[B]ack'], (f'Create work order', body, f'Work order with the ID {workOrderInstance.id} has been succesfully created!\nChoose a option: '))
    




    def editWorkOrder(self) -> str:
        '''USER asked what work order he wants  to edit, and allows him to choose what and enters a new value, 'q' or 'b' is returned based on users options'''
         # Getting all work orders that an employee has not assigned himself too

        WorkOrder = None
        lookUpWorkOrderId = self.takeInputAndPrintMenuWithoutBrackets('', ('Edit work orders', ['Search for a CURRENT work order', 'That is a work order that a employee has not assigned himself to'], 'Enter a work order ID: '))
        while not WorkOrder: # while loop continues while the id that the user enters doesnt match any of the current work orders id's
            if lookUpWorkOrderId.lower() in quirOrBack:
                return lookUpWorkOrderId.lower()
            # check whether a work order exists with the loop up id the user entered, 0 is returned if not
            WorkOrder = self.logicWrapper.listWorkOrders(id = lookUpWorkOrderId, userID = 0) 
            if not WorkOrder:
                # if a current work order is not found then the user is asked again
                lookUpWorkOrderId = self.takeInputAndPrintMenuWithoutBrackets('', ('Edit work orders', ['Search for a CURRENT work order', 'That is a work order that a employee has not assigned himself to'], 'A current work order with that ID doesnt exist, please try again\nEnter a work order ID: '))
        
        WorkOrderInstance = WorkOrder[0]
 

        # Getting the property assigned to the work order:
        property = self.logicWrapper.listProperties(id = WorkOrderInstance.propertyNumber)

        # creating a dictionary that holds all editable values, different dictionaries based on whether a constructor was assigned or not
        # if there is no contractor then the dictionary keeping track needs to be slightly different
        if WorkOrderInstance.contractorID != -1: 
            contractor = self.logicWrapper.listContractors(id = WorkOrderInstance.contractorID)    
            workOrderDict = {'description': WorkOrderInstance.description, 'property number': WorkOrderInstance.propertyNumber, 'priority': WorkOrderInstance.priority, 'contractor': contractor[0].name, 'room id': WorkOrderInstance.roomFacilityId}
        else:
            workOrderDict = {'description': WorkOrderInstance.description, 'property number': WorkOrderInstance.propertyNumber, 'priority': WorkOrderInstance.priority, 'contractor': 'No contractor assigned to this work order', 'room id': WorkOrderInstance.roomFacilityId}

        valueToChange = ''
        # keep asking the user what he wants to change until he enters a value that is in the global variable list that has all availavle edit options
        while valueToChange.lower() not in AVAILABLE_EDIT_OPTIONS: 
            valueToChange = self.takeInputAndPrintMenuWithoutBrackets([], ('Edit work orders', [f'{key}: {value}' for key, value in workOrderDict.items()], 'Choose what value to change: '))
            if valueToChange.lower() in quirOrBack:
                return valueToChange.lower()

        # match casing all the values that the user wants to change
        match valueToChange.lower():
            case 'description':
                newValue = self.getValidInput('Edit work orders', 'Write a new description for this work order: ', validation.validateText, workOrderDict)
                if newValue.lower() in quirOrBack:
                    return newValue.lower()
                # change the value, send new value down to logic layer
                self.logicWrapper.editWorkOrder(entry='id', entryValue=WorkOrderInstance.id, description = newValue)
            
            case 'property number':
                newProperty = []
                newValue = self.getValidInput('Edit work orders', 'Write a new property number for this work order: ', validation.validateText, workOrderDict) # Ask the user for a property number 
                while not newProperty: # While loops keeps going until the wrapper is able return a property instance, it only returns a instance when a correct property number is entered
                    if newValue.lower() in quirOrBack:
                        return newValue.lower()
                     # Check whether a property exists with the number, if it doesnt the none is returened
                    newProperty = self.logicWrapper.listProperties(id = newValue)
                    if not newProperty:
                        # ask the user again if none was returned then the user is asked again
                        newValue = self.getValidInput('Edit work orders', 'This property number doesnt exist!\nWrite a new property number for this work order: ', validation.validateText, workOrderDict) # Ask the user for a property number
                self.logicWrapper.editWorkOrder(entry='id', entryValue=WorkOrderInstance.id, property = newProperty[0].id)

            case 'priority':
                # ask the user for a new priority, validaring it and printing menu
                newValue = self.getValidInput('Edit work orders', 'Choose a new priority(Emergency, now, not later than tommorow): ', validation.validatePriority, workOrderDict, 'Please choose from the options in the brackets\n')
                if newValue.lower() in quirOrBack: # go back one menu or quit
                    return newValue.lower()
                # update with new priority, sending new value to logic wrapper and logic layer
                self.logicWrapper.editWorkOrder(entry='id', entryValue=WorkOrderInstance.id, priority = newValue)
            
            case 'contractor':
                contractor = []
                while not contractor: # While loop continues until a contractor is chosen that is within the system
                    # print all contractors available and make the user choose
                    newValue = self.showContractorsInfo('Choose a new contractor: ', '')
                    if newValue.lower() in quirOrBack:
                            return newValue.lower()
                    # send the id chocsen by the user to logic layer and see if the id exists in the system, none is returned if it doesnt
                    contractor = self.logicWrapper.listContractors(id = newValue)
                    # change the value by senfing to logic layer
                self.logicWrapper.editWorkOrder(entry='id', entryValue=WorkOrderInstance.id, contractorID = newValue)
                newValue = contractor[0].name
            
            case 'room id':
                newValue = ''
                while not newValue: # While loop continues until enters a valid id for either room or facility
                    roomOrfacility = self.takeInputAndPrintMenu([], ('Edit work orders', [f'{key}: {value}' for key, value in workOrderDict.items()], 'Room or facility?: ')) # Ask the manager whether a facility or a room needs fixing
                    if roomOrfacility.lower() in quirOrBack:
                        return newValue.lower()
                    # get the id that keeps track of room and id's based on what the user chose,this dict is used to keep track of user input and print menu
                    match roomOrfacility.lower(): 
                        case 'room':
                            idDict = property[0].rooms # if the manager chose a room then we use the room id dict
                        case 'facility':
                            idDict = property[0].facilities # if the manager chose a facility then we use the facility dict
                        case _:
                            continue
                    newValue = ''
                    # keep asking the user for a new id until her chooses something from the available options that are being printed
                    while newValue not in idDict:  
                        newValue = self.takeInputAndPrintMenu('', ('Edit work orders', [f'{value}: {key}' for key, value in idDict.items()], 'Choose a new ID: '))
                        if newValue.lower() in quirOrBack:
                            return newValue.lower()
                    # change the value by sending to logic layer
                self.logicWrapper.editWorkOrder(entry='id', entryValue=WorkOrderInstance.id, roomFacilityId = newValue)
                
        workOrderDict[valueToChange.lower()] = newValue

        # printing menu with all the new values and asking user to either quit or go back
        return self.takeInputAndPrintMenuWithoutBrackets(['Quit', 'Back'], (f'Create work order', [f'{key}: {value}' for key, value in workOrderDict.items()], f'Work order information has been succesfully updated!\nChoose a option: '))


    def completedWorkOrder(self) -> str:
        '''Managers marks work reports sent by employees as complete, user either returns 'q', or 'b' based on whether he quits or backs'''
        uncompleteList: list = self.logicWrapper.listWorkReports(isCompleted=False)

        # body is used to keep to print body of menu
        body = self.showWorkReports(uncompleteList)

        # if there are no work reports to print the user is notified by that and can either quit or exit
        if not body:
            return self.takeInputAndPrintMenuWithoutBrackets(['Quit', 'Back'], (f'Create work order', ['There are no work orders you can currently mark as complete!'], f'Choose a option: '))
        
        # based on the work reports the manger can choose from , a list is created to keep track of what the user can input as the work report to mark as complete
        uncompleteIdList = [str(instance.id) for instance in uncompleteList]

        retVal = ''
        prompt = 'Choose a work report ID you want to mark as finished\nChoose a option: '
        # Keep asking the user for a id until he enters a valid id from the id's the logic layer sent
        while retVal not in uncompleteIdList:
            retVal = self.takeInputAndPrintMenuWithoutBrackets([], ('Complete work reports', body, prompt)) 
            if retVal.lower() in quirOrBack:
                return retVal.lower()
            prompt = 'Choose a work report ID you want to mark as finished\nPlease choose a ID from the available work reports: '

        workReport = self.logicWrapper.listWorkReports(id = retVal)
        # allow the manager to leave an additional comment
        additionalComment = self.takeInputAndPrintMenuWithoutBrackets([], ('Complete work reports', body, 'Add a additional comment: '))

        # change values of work report and work order instances by calling logic wrapper
        self.logicWrapper.editWorkReports(entry='id', entryValue = int(retVal), isCompleted = True)
        self.logicWrapper.editWorkReports(entry='id', entryValue = int(retVal), comment = additionalComment)
        self.logicWrapper.editWorkOrder(entry='id', entryValue=workReport[0].workOrderID, isCompleted = True)

        return self.takeInputAndPrintMenuWithoutBrackets(['Quit', 'Back'], (f'Create work order', [f'Work report {workReport[0].id} has been marked as complete!'], f'Choose a option: '))





