from ui.baseUI import BaseUI
from ui.validationUI import ValidationUI
from logic.logicWrapper import Logic_Wrapper
validation = ValidationUI()


class SearchUI(BaseUI):
    def __init__(self, logicWrapper: Logic_Wrapper):
        self.logicWrapper = logicWrapper

    def employeeSearch(self):
        options = ['[K]ennitala search', '[L]ocation search']
        userOption = self.takeInputAndPrintMenu(options, ('Employee search', options, 'Choose a option'))


        if userOption.lower() == 'k':
            returnValue = self.showEmployeeID()
        else:
            returnValue = self.showEmployeesLocation()

        return returnValue




    def showEmployeeID(self):
        # use Search class there is Employee Search class there that can search by any param in this case kennitala
        employee = []
        while not employee:
            lookUpKennitala = self.getValidInput("look for employee","Enter ID: ", validation.validateKennitala)
            match lookUpKennitala.lower():
                case 'q':
                    return 'q' # quit the whole program
                case 'b':
                    return False # Go back one page
    
            employee = self.logicWrapper.listEmployees(kennitala=lookUpKennitala)  # Call the wrapper that is 

        employee_list = [f'{key}: {value}' for key, value in list(employee[0].__dict__.items())[1:]]

        return self.takeInputAndPrintMenu(['[Q]'], ('look for employee', employee_list, 'Choose a option: '))




    
    def showEmployeesLocation(self):
        # use Search class there is Employee Search class there that can search by any param in this case kennitala
        employee = []
        while not employee:
            lookUpLocation = self.getValidInput("look for employee","Enter Location: ", validation.validateText)
            match lookUpLocation.lower():
                case 'q':
                    return 'q' # quit the whole program
                case 'b':
                    return False # Go back one page
    
            employees = self.logicWrapper.listEmployees(location=lookUpLocation)  




    def propertySearch(self):
                # use Search class there is Employee Search class there that can search by any param in this case kennitala
        userOption = self.takeInputAndPrintMenu( ['[L]ocation search', '[P]roperty number search'], ('View property', ['[L]ocation search', '[P]roperty number search'], "Choose a option: "))

        match userOption.lower():
            case 'q':
                return 'q'
            case 'b':
                return False
            case 'l':
                self.showEmployeesLocation()
            case 'p':
                self.showropertyNumberSearch()



        # talk to wrapper with the kennitala entered THIS NEEDS TO GET SORTED :)


    def showPropertyLocationSearch(self):

        lookUpPropertiesOnLocation = self.getValidInput('View property', 'Enter a location: ', validation.validateLocation)
        propertyInformation = self.logicWrapper.searchProperties(Location = lookUpPropertiesOnLocation)

  
    def showropertyNumberSearch(self):
        lookUpPropertyNumber = self.getValidInput('View property', 'Enter a location', validation.validatePropertyNumber)
        propertyInfromation = self.logicWrapper.searchProperties(propertyNumber = lookUpPropertyNumber)








    def workOrderSearch(self):
        options = ['[I]D search', '[P]roperty number search', '[K]ennitala search']
        userOption = self.takeInputAndPrintMenu(options, ('Search work order', options, 'Choose a option:  '))
        work_orders = []

        match userOption.lower():
            case 'i':
                userId = self.takeInputAndPrintMenu([], ('Search Work orders','', 'Enter a work order ID: '))
                workOrdersInfo = self.logicWrapper.searchWorkOrders(workOrderId = userId)
            case 'p':
                propertyNumber = self.takeInputAndPrintMenu([], ('Search Work orders','', 'Enter a property Number: '))
                workOrdersInfo = self.logicWrapper.searchWorkOrders(properyNum = propertyNumber)
            case 'k':
                kennitala = self.takeInputAndPrintMenu([], ('Search Work orders','', 'Enter a kennital: '))
                workOrdersInfo = self.logicWrapper.searchWorkOrders(Kennitala = kennitala)
            
                

    def workReportSearch(self):
        options = ['[I]D search', '[P]roperty number search', '[K]ennitala search']
        userOption = self.takeInputAndPrintMenu(options, ('Search work report', options, 'Choose a option:  '))
        work_orders = []

        match userOption.lower():
            case 'i':
                userId = self.takeInputAndPrintMenu([], ('Search Work reports','', 'Enter a work order ID: '))
                workOrdersInfo = self.logicWrapper.searchWorkReports(workOrderId = userId)
            case 'p':
                propertyNumber = self.takeInputAndPrintMenu([], ('Search Work reports','', 'Enter a property Number: '))
                workOrdersInfo = self.logicWrapper.searchWorkReports(properyNum = propertyNumber)
            case 'k':
                kennitala = self.takeInputAndPrintMenu([], ('Search Work reports','', 'Enter a kennital: '))
                workOrdersInfo = self.logicWrapper.searchWorkReports(Kennitala = kennitala)
    



  

    def workReportSearch():
        pass

    def contractors():
        pass


    def getValidInput(self, name, prompt, validationFunc, userDict: dict = {}) -> str:
        '''Validates the input based on the validation function given, prints baseMenu every time the user enters unvalid info. menu is based on the arguments given '''
        while True:
            self.printBaseMenu(name, [f'{key}: {value}' for key, value in userDict.items()], prompt)
            user_input = input(' ')
        
            if validationFunc(user_input):
                return user_input
