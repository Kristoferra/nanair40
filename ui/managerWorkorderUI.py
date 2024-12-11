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

    def addNewWorkOrder(self):
        body = []
        Userdescription = self.takeInputAndPrintMenuWithoutBrackets('', ('Create work order', '', 'Description of work order: ')) # Get a description on what needs to be done
        if Userdescription in quirOrBack:
            return Userdescription
        body.append(f'Work description: {Userdescription}')

        property = [] 
        lookUpPropertyNumber = self.takeInputAndPrintMenuWithoutBrackets('', ('Create work order', body, 'Enter a property number: ')) # Ask the user for a property number
        while not property: # While loops keeps going until the wrapper is able return a property instance, it only returns a instance when a correct property number is entered
            lookUpPropertyNumber = self.takeInputAndPrintMenu('', ('Create work order', body, 'Enter a property number')) # Ask the user for a property number
            if lookUpPropertyNumber in quirOrBack:
                return lookUpPropertyNumber
            property = self.logicWrapper.listProperties(id = lookUpPropertyNumber) # Check whether a property exists with the number, if it does then a list of a single isntance is returned
            if not property:
                lookUpPropertyNumber = self.takeInputAndPrintMenuWithoutBrackets('', ('Create work order', body, 'A property doesnt exist with that property number\nEnter a property number: ')) # Ask the user for a property number

        body.append(f'Property Number: {lookUpPropertyNumber}')
        managerRoomFacilityId = ''
        roomOrfacility = self.takeInputAndPrintMenuWithoutBrackets('', ('Create work order', body, 'Room or facility?: ')) # Ask the manager whether a facility or a room needs fixing
        while not managerRoomFacilityId: # While loop continues until enters a valid id for either room or facility
            roomOrfacility = self.takeInputAndPrintMenu('', ('Create work order', body, 'Room or facility?: ')) # Ask the manager whether a facility or a room needs fixing
            if roomOrfacility in quirOrBack:
                return roomOrfacility
            match roomOrfacility.lower(): 
                case 'room':
                    idDict = property[0].rooms # if the manager chose a room then we use the room id dict
                case 'facility':
                    idDict = property[0].facilities # if the manager chose a facility then we use the facility dict
                case _:
                    roomOrfacility = self.takeInputAndPrintMenuWithoutBrackets('', ('Create work order', body, 'Please pick either room or facility\nRoom or facility?: ')) # Ask the manager whether a facility or a room needs fixing
                    continue

            managerRoomFacilityId = self.takeInputAndPrintMenuWithoutBrackets('', ('Create work order', [f'{value}: {key}' for key, value in idDict.items()], 'Choose a ID: '))
            while managerRoomFacilityId not in idDict: # print a menu with all the id's the user can choose from, while loop continues until the user enters a id that matches a id in the dictionary
                managerRoomFacilityId = self.takeInputAndPrintMenuWithoutBrackets('', ('Create work order', [f'{value}: {key}' for key, value in idDict.items()], 'Please choose a valid ID from the options above\nChoose a ID: '))
                if managerRoomFacilityId in quirOrBack:
                    return managerRoomFacilityId
            

        body.append(f'Room/facility id: {managerRoomFacilityId}')
            
        priority = False
        userPriority = self.takeInputAndPrintMenuWithoutBrackets('', ('Create work order', body, 'How important? (Emergency, now, as soon as possible): '))
        while not priority: # While loop continues until the user enters a valid priority description
            userPriority = self.takeInputAndPrintMenu('', ('Create work order', body, 'How important? (Emergency, now, not later than tommorow): '))
            if userPriority in quirOrBack:
                return userPriority
            if validation.validatePriority(userPriority):
                priority = True
            else:
                userPriority = self.takeInputAndPrintMenuWithoutBrackets('', ('Create work order', body, 'Please choose one of three available options\nHow important? (Emergency, now, as soon as possible): '))

        body.append(f'Priority: {userPriority}') 

        
            
        isContractor = self.takeInputAndPrintMenuWithoutBrackets(['Y', 'N'], ('Create work order', body, 'Contractor? (Y/N): ')) # The manager either chooses yes that there is a contracor or no that there isnt
        if isContractor.lower() in quirOrBack:
            return isContractor.lower()
        lookUpContractor = -1
        if isContractor.lower() == 'y': # if there is a contractor then the following if statement applies
            contractor = []
            while not contractor: # While loop continues until a contractor is chosen that is within the system
                lookUpContractor = self.showContractorsInfo('Choose a contractor ID: ', '')
                if lookUpContractor in quirOrBack:
                    return lookUpContractor
                contractor = self.logicWrapper.listContractors(id = lookUpContractor)
            
            body.append(f'Contractor: {contractor[0].name}')


        ### Maybe add a date function??

        isRecuring = self.takeInputAndPrintMenu(["Y", "N"], ("Add work ordder", body, "IS this task reccurong(Y/N): "))
        repeating = False
        repeatInterval = 0
        if isRecuring.lower() == "y":
            repeating = True
        if repeating:
            self.takeInputAndPrintMenu(["D", "W", "M", "Y"], ("Create a work order", ["[D]aily", "[W]eekly", "[M]onthly", "[Y]early"], "Choose option: "))
            repeatInterval = 2 # to be changed


        self.logicWrapper.currentWorkOrderID+=1
        workOrderInstance = WorkOrder(id=self.logicWrapper.currentWorkOrderID, description=Userdescription, propertyNumber=lookUpPropertyNumber, priority = userPriority, contractorID=int(lookUpContractor), roomFacilityId= managerRoomFacilityId, repeating=repeating, repeatInterval=repeatInterval)


        self.logicWrapper.addWorkOrder(workOrderInstance)
       

        return self.takeInputAndPrintMenu(['[Q]uit', '[B]ack'], (f'Create work order', body, f'Work order with the ID {workOrderInstance.id} has been succesfully created!\nChoose a option: '))
    




    def editWorkOrder(self):
         # Getting all work orders that an employee has not assigned himself too

        WorkOrder = None
        while not WorkOrder: # while loop continues while the id that the user enters doesnt match any of the current work orders id's
            lookUpWorkOrderId = self.takeInputAndPrintMenu('', ('Edit work orders', ['Search for a CURRENT work order', 'That is a work order that a employee has not assigned himself to'], 'Enter a work order ID: '))
            if lookUpWorkOrderId.lower() in quirOrBack:
                return lookUpWorkOrderId.lower()
            WorkOrder = self.logicWrapper.listWorkOrders(id = lookUpWorkOrderId, userID = 0)
        
        WorkOrderInstance = WorkOrder[0]
 

        # Getting the property assigned to the work order:
        property = self.logicWrapper.listProperties(id = WorkOrderInstance.propertyNumber)

        # creating a dictionary that holds all editable values, different dictionaries based on whether a constructor was assigned or not
        if WorkOrderInstance.contractorID != -1:
            contractor = self.logicWrapper.listContractors(id = WorkOrderInstance.contractorID)    
            workOrderDict = {'description': WorkOrderInstance.description, 'property number': WorkOrderInstance.propertyNumber, 'priority': WorkOrderInstance.priority, 'contractor': contractor[0].name, 'room id': WorkOrderInstance.roomFacilityId}
        else:
            workOrderDict = {'description': WorkOrderInstance.description, 'property number': WorkOrderInstance.propertyNumber, 'priority': WorkOrderInstance.priority, 'contractor': 'No contractor assigned to this work order', 'room id': WorkOrderInstance.roomFacilityId}

        valueToChange = ''
        while valueToChange.lower() not in AVAILABLE_EDIT_OPTIONS: # keep asking the user what he wants to change until he enters a value that is in the global variable list that has all availavle edit options
            valueToChange = self.takeInputAndPrintMenu([], ('Edit work orders', [f'{key}: {value}' for key, value in workOrderDict.items()], 'Choose what value to change: '))
            if valueToChange.lower() in quirOrBack:
                return valueToChange.lower()

        match valueToChange.lower():
            case 'description':
                newValue = self.getValidInput('Edit work orders', 'Write a new description for this work order: ', validation.validateText, workOrderDict)
                if newValue.lower() in quirOrBack:
                    return newValue.lower()
                self.logicWrapper.editWorkOrder(entry='id', entryValue=WorkOrderInstance.id, description = newValue)
            
            case 'property number':
                newProperty = [] 
                while not newProperty: # While loops keeps going until the wrapper is able return a property instance, it only returns a instance when a correct property number is entered
                    newValue = self.getValidInput('Edit work orders', 'Write a new property number for this work order: ', validation.validateText, workOrderDict) # Ask the user for a property number
                    if newValue.lower() in quirOrBack:
                        return newValue.lower()
                    newProperty = self.logicWrapper.listProperties(id = newValue) # Check whether a property exists with the number, if it does then a list of a single isntance is returned
                self.logicWrapper.editWorkOrder(entry='id', entryValue=WorkOrderInstance.id, property = newProperty[0].id)

            case 'priority':
                newValue = self.getValidInput('Edit work orders', 'Choose a new priority(Emergency, now, not later than tommorow): ', validation.validatePriority, workOrderDict)
                if newValue.lower() in quirOrBack:
                    return newValue.lower()
                self.logicWrapper.editWorkOrder(entry='id', entryValue=WorkOrderInstance.id, priority = newValue)
            
            case 'contractor':
                contractor = []
                while not contractor: # While loop continues until a contractor is chosen that is within the system
                    newValue = self.showContractorsInfo('Choose a new contractor: ', '')
                    if newValue.lower() in quirOrBack:
                            return newValue.lower()
                    contractor = self.logicWrapper.listContractors(id = newValue)
                self.logicWrapper.editWorkOrder(entry='id', entryValue=WorkOrderInstance.id, contractorID = newValue)
                newValue = contractor[0].name
            
            case 'room id':
                newValue = ''
                while not newValue: # While loop continues until enters a valid id for either room or facility
                    roomOrfacility = self.takeInputAndPrintMenu([], ('Edit work orders', [f'{key}: {value}' for key, value in workOrderDict.items()], 'Room or facility?: ')) # Ask the manager whether a facility or a room needs fixing
                    if roomOrfacility.lower() in quirOrBack:
                        return newValue.lower()
                    match roomOrfacility.lower(): 
                        case 'room':
                            idDict = property[0].rooms # if the manager chose a room then we use the room id dict
                        case 'facility':
                            idDict = property[0].facilities # if the manager chose a facility then we use the facility dict
                        case _:
                            continue
                    newValue = ''
                    while newValue not in idDict:  
                        newValue = self.takeInputAndPrintMenu('', ('Edit work orders', [f'{value}: {key}' for key, value in idDict.items()], 'Choose a new ID: '))
                        if newValue.lower() in quirOrBack:
                            return newValue.lower()
                self.logicWrapper.editWorkOrder(entry='id', entryValue=WorkOrderInstance.id, roomFacilityId = newValue)
                
        workOrderDict[valueToChange.lower()] = newValue
        return self.takeInputAndPrintMenu(['Quit', 'Back'], (f'Create work order', [f'{key}: {value}' for key, value in workOrderDict.items()], f'Work order information has been succesfully updated!\nChoose a option: '))


    def completedWorkOrder(self):
        uncomplete: list = self.logicWrapper.listWorkReports(isCompleted=False)
        body = self.showWorkReports(uncomplete)
        retVal = self.takeInputAndPrintMenuWithoutBrackets([], ('Complete work reports', body, 'Choose a work report you want to mark as finished!\nVhoose a option:'))
        for unc in uncomplete:
            if retVal == str(unc.id):
                pass

