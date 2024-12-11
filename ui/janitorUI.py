from ui.baseUI import BaseUI
from baseClasses.workOrder import WorkOrder  
from baseClasses.workReport import WorkReport
from logic.logicWrapper import Logic_Wrapper
from ui.searchUI import SearchUI
import os
quitOrBack = ['q', 'b']

class JanitorUI(SearchUI):
    def __init__(self, logicWrapper: Logic_Wrapper):
        self.logicWrapper = logicWrapper



    def workOrders(self):
        filter = self.takeInputAndPrintMenu(['P', 'A'], ('Work orders', ['Property', 'All work orders'], 'Choose what you would like to filter by: '))
        match filter.lower():
            case 'p':
                property = []
                propertyList = self.logicWrapper.listProperties()
                prompt = 'Enter a property number you would like to see work orders from: '
                while not property:
                    lookUpProperty = self.showPropertyInfo(propertyList, '', prompt)
                    property = self.logicWrapper.listProperties(id = lookUpProperty)
                    prompt = 'Please enter a property number from the options above\nEnter a property number you would like to see work orders from: '
                currentWorkOrders = self.logicWrapper.listWorkOrders(userID = 0, isCompleted = False, propertyNumber = lookUpProperty)
            case 'a':
                currentWorkOrders = self.logicWrapper.listWorkOrders(userID = 0, isCompleted = False)








        # get all work orders that an employee has not assigned himslef to.
        body = self.showWorkOrders(currentWorkOrders) # get the table of what should be printed out
        if not body: # if the body is empty that means there are no current work orders, if so we ask the user ot qquit or go back
            return self.takeInputAndPrintMenu(['[Q]uit', '[B]ack'], ("Work Orders", ['There are no current work orders!'], f'Choose a option'))
        
        workOrderIdList = [str(instance.id) for instance in currentWorkOrders] # Get all id's of the current work orders

        userOrderId = ''
        while userOrderId not in workOrderIdList: # while loop continues and keeps asking the user for a ID until the user enters a ID that isa available 
            userOrderId = self.takeInputAndPrintMenuWithoutBrackets('', ("Work Orders", body, 'Choose a ID to work on: '))
            if userOrderId.lower() in quitOrBack:
                return userOrderId

        employeeId = ''
        lookUpkennitala = self.takeInputAndPrintMenuWithoutBrackets('', ("Work Orders", body, 'Enter a employee kennitala to asign the work order to: '))
        while not employeeId:
            lookUpkennitala = self.takeInputAndPrintMenu('', ("Work Orders", body, 'Enter a employee kennitala to asign the work order to: '))
            if lookUpkennitala.lower() in quitOrBack:
                return lookUpkennitala
            employeeId = self.logicWrapper.listEmployees(kennitala = lookUpkennitala)
            if not employeeId:
                lookUpkennitala = self.takeInputAndPrintMenuWithoutBrackets('', ("Work Orders", body, 'No employee in the system has this kennitala\nEnter a employee kennitala to asign the work order to: '))

        self.logicWrapper.editWorkOrder('id', int(userOrderId), userID = lookUpkennitala)

        currentWorkOrders = self.logicWrapper.listWorkOrders(userID = 0)
        newBody = self.showWorkOrders(currentWorkOrders)
        if newBody is None:
            return self.takeInputAndPrintMenuWithoutBrackets(['[Q]uit', '[B]ack'], ("Work Orders", [''], f'Employee {employeeId[0].name} has succesfully assigned himself to the work order\nChoose a option: '))

        return self.takeInputAndPrintMenuWithoutBrackets(['[Q]uit', '[B]ack'], ("Work Orders", newBody, f'Employee {employeeId[0].name} has succesfully assigned himself to the work order\nChoose a option: '))



    def addWorkReport(self) -> str:
        '''Lists all work orders that are not complete and have been signed to a employee, the user is asked for what work report he wants to work, user writes a work report on that work order and then returns'''
        filter = self.takeInputAndPrintMenu(['P', 'A'], ('Work orders', ['Property', 'All work orders'], 'List work orders that you can create a report on\nChoose what you would like to filter by: '))
        match filter.lower():
            case 'p':
                property = []
                propertyList = self.logicWrapper.listProperties()
                prompt = 'Enter a property number you would like to see work orders from: '
                while not property:
                    lookUpProperty = self.showPropertyInfo(propertyList, '', prompt)
                    property = self.logicWrapper.listProperties(id = lookUpProperty)
                    prompt = 'Please enter a property number from the options above\nEnter a property number you would like to see work orders from: '
                currentWorkOrders = self.logicWrapper.listWorkCurrentWorkOrders(isCompleted = False, propertyNumber = lookUpProperty)
            case 'a':
                currentWorkOrders = self.logicWrapper.listWorkCurrentWorkOrders(isCompleted = False)


        body = self.showWorkOrders(currentWorkOrders) # call the show work orders function and get a string of all work orders and theit info
        if not body:
            return self.takeInputAndPrintMenu(['[Q]uit', '[B]ack'], ("Create a work report", ['Currently there are no work orders to make a report on!'], 'Choose a option: '))
        availableWorkOrderIds = [str(instance.id) for instance in currentWorkOrders] # list of all id's the user can choose from


        WorkOrderId = ''
        # the user is asked for a work ID until her enters a id that is on of the ids that the logic layer gives
        while WorkOrderId not in availableWorkOrderIds: 
            # ask the user for an id until he enters an id in the list
            WorkOrderId =  self.takeInputAndPrintMenu('', ('Create a work report', body, 'Choose a Work order to make a report on: '))
            if WorkOrderId.lower() in quitOrBack: # if user enters to quit or go back, we return that
                return WorkOrderId.lower()
        
        workOrder = self.logicWrapper.listWorkOrders(id = WorkOrderId) # get all work orders listed to the id
        employee = self.logicWrapper.listEmployees(kennitala = workOrder[0].userID) # get the epmloyee that is assigned to the work order
        now = datetime.now()
        # create a dictionary that keeps track of all values the user enters in related to the dict
        workReportDict = {'Work order id': WorkOrderId, 'Empbloyee': employee[0].name, 'date': now, 'Description': '', 'contractor': '---','cost': ''}

        # if the contractor ID is not -1, then this report has a contractor and we have to upadate what we print out on the screen
        if int(workOrder[0].contractorID) != -1:
            contractor = self.logicWrapper.listContractors(id = workOrder[0].contractorID)
            workReportDict['contractor'] = contractor[0].name

        # print the menu and ask the user for a dedscription for the work report
        workReportDict['Description'] = self.getValidInput('Create work report', 'Write a desription for the work order: ', validation.validateText, workReportDict)

        if workReportDict['Description'].lower() in quitOrBack: # if the user entered to  quit ot go back we return that
            return workReportDict['Description'].lower()

        # ask the user for a total cost related to the work order
        workReportDict['cost'] = self.getValidInput('Create work report', 'Write the total cost for the work: ', validation.validateNumber, workReportDict, 'Please only enter a number in kr\n') 
        if workReportDict['cost'].lower() in quitOrBack:
            return workReportDict['cost'].lower()
        
        # add a kr sign to the end, so that it look better when printing out
        

        # create a work report instance that will be sent down to logic layer and then stored in a json file
        WorkOrderId = int(WorkOrderId)
        now = now.strftime("%d.%m.%Y")
        workReportID: int = self.logicWrapper.currentWorkReportID(WorkOrderId)
        WorkReportInstance = WorkReport(workReportID, WorkOrderId, workReportDict['Description'], int(workOrder[0].contractorID), workOrder[0].userID, int(workReportDict['cost']))
        workReportDict['cost'] += 'Kr'
        self.logicWrapper.addWorkReport(WorkReportInstance)


        self.logicWrapper.editWorkOrder(entry='id', entryValue=workOrder[0].id, sentToManager = True)
        # create a list if strings that will be pirnted out in the body of next menu
        workReportList = [f'{key}: {value}' for key, value in workReportDict.items()]
        return self.takeInputAndPrintMenu(['[Q]uit', '[B]ack'], ("Work Orders", workReportList, f'Work report has been created succesfully!\nChoose a option'))


        

        


