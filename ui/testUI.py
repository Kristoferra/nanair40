from ui.propertiesUI import PropertiesUI
from ui.testBaseUI import BaseUI
from ui.employeeUI import EmployeeUI
from ui.contractorsUI import ContractorsUI
from ui.janitorUI import JanitorUI
from ui.searchUI import SearchUI
from logic.logicWrapper import Logic_Wrapper
from ui.managerWorkorderUI import ManagerWorkOrder

class MainUI(BaseUI):
    def __init__(self):
        self.logicWrapper = Logic_Wrapper()
        self.baseUI = BaseUI()
        self.employeeUI = EmployeeUI(self.logicWrapper)
        self.contractorsIU = ContractorsUI(self.logicWrapper)
        self.propertiesUI = PropertiesUI(self.logicWrapper)
        self.managerWorkOrderUI = ManagerWorkOrder(self.logicWrapper)
        self.janitorUI = JanitorUI(self.logicWrapper)
        self.searchUI = SearchUI(self.logicWrapper)

    def mainMenu(self, error=False) -> None:
        self.printMainMenu() 
        possibilites = ['M', 'J', 'S']
        functions = [self.ShowManagerMenu, self.ShowMaintenanceMenu, self.ShowSearchMenu]
        optionInput = input(' ')
        return self.returnTable(optionInput, None, possibilites, functions)


    def ShowManagerMenu(self, error=False) -> None:
        options = ['Employee menu', 'Properties menu', 'Work orders menu', 'Contractors']
        functions = [self.employeeMenu, self.propertiesMenu, self.workOrderMenu, self.contractorsIU.showContractor]
        optionInput = input("ENT:")
       #self.takeInputAndPrintMenu(options, ('Manager', options, 'Choose a option: '))
        return self.returnTable(optionInput, self.mainMenu, options, functions)


    def employeeMenu(self) -> None:
        options = ['Add employee', 'Edit employee', 'List employees']
        functions = [self.employeeUI.addEmployee, self.employeeUI.showEmployee, self.employeeUI.showEmployees]
        optionInput = input("ENT:")
        #optionInput = self.takeInputAndPrintMenu(options, ('Employee menu', ['[A]dd employee', '[E]dit employee', '[L]ist employees'], 'Choose a option'))

        return self.returnTable(optionInput, self.ShowManagerMenu, options, functions)



    def propertiesMenu(self) -> str:
        optionInput = ''
        while optionInput.lower() != 'q':
            options = ['Add property', 'Edit property', 'List properties']


            optionInput = self.takeInputAndPrintMenu(options, ('Properties menu', options, 'Choose a option'))
            

            match optionInput.lower():
                case 'a':
                    returnValue = self.propertiesUI.addProperty()    
                case 'e':
                    returnValue = self.propertiesUI.showProperty()
                case 'l':
                    returnValue = self.propertiesUI.listProperties()
                case 'b':
                    return False

                case 'q':  # Matching case for comparison
                    return 'q'


            if returnValue == 'q':
               return 'q'


           
    def workOrderMenu(self) -> str | bool:
        optionInput = ''
        while optionInput.lower() != 'q':
            options = ['Add work order', 'Completed work reports', 'Edit/view work orders']

            optionInput = self.takeInputAndPrintMenu(options, ('Work order menu', options, 'Choose a option'))

            match optionInput.lower():
                case 'a':
                    returnValue = self.managerWorkOrderUI.addNewWorkOrder()
                case 'e':
                    returnValue = self.managerWorkOrderUI.editWorkOrder()
                case 'c':
                    returnValue = self.managerWorkOrderUI.completedWorkOrder()
                case 'b':
                    return False
                case 'q':  # Matching case for comparison
                    return 'q'


            if returnValue == 'q':
               return 'q'


        





    def ShowMaintenanceMenu(self) -> str | bool:
        optionInput = ''
        while optionInput.lower() != 'q':
            options = ['Work orders', 'Create work report']

            optionInput  = self.takeInputAndPrintMenu(options, ('Janitor Menu', options, 'Choose a option'))

            match optionInput.lower():
                case 'w':
                    returnValue = self.janitorUI.workOrders()
                case 'c':
                    returnValue = self.janitorUI.addWorkReport()
                case 'b':
                    return False

                case 'q':  # Matching case for comparison
                    return 'q'

            if returnValue == 'q':
               return 'q'


            
    def ShowSearchMenu(self) -> str | bool:

        optionInput = ''
        while optionInput.lower() != 'q':
            options = ['Employee Search', 'Property search', 'Work order search', 'Report search', 'Contractors']

            optionInput = self.takeInputAndPrintMenu(options, ('Search menu', options, 'Choose a option'))
 

            match optionInput.lower():
                case 'e':
                    returnValue = self.searchUI.employeeSearch()
                case 'p':
                    returnValue = self.searchUI.propertySearch()
                case 'w':
                    returnValue = self.searchUI.workOrderSearch()
                case 'r':
                    returnValue = self.searchUI.workReportSearch()
                case 'c':
                    returnValue = self.searchUI.showContractorsInfo()
                case 'b':
                    return False
                case 'q':  # Matching case for comparison
                    return 'q'

            if returnValue == 'q':
               return 'q'
