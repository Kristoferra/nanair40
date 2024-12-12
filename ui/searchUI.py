from ui.baseUI import BaseUI
from ui.validationUI import ValidationUI
from logic.logicWrapper import Logic_Wrapper
from baseClasses.workOrder import WorkOrder
from baseClasses.Employee import Employee
from baseClasses.Property import Property
from baseClasses.workReport import WorkReport
validation = ValidationUI()
quitOrback = ['q', 'b', 'Q', 'B']




class SearchUI(BaseUI):
    def __init__(self, logicWrapper: Logic_Wrapper = None):
        self.logicWrapper = logicWrapper

    def employeeSearch(self) -> str | bool:
        options = ['Kennitala search', 'Location search']

        while True:
            userOption = self.takeInputAndPrintMenu(options, ('Employee search', options, 'Choose a option'))
            if userOption.lower() in quitOrback:
                return userOption.lower()
            match userOption.lower():
                case 'k':
                    returnValue = self.showEmployeeID()
                case 'l':
                    employee_list = []
                    locations = self.logicWrapper.listLocations()
                    locationsList = [location.airport for location in locations]
                    prompt = 'Enter a location: '
                    while not employee_list:
                        lookUpLocation = self.takeInputAndPrintMenuWithoutBrackets("", ('Employee search by location', locationsList, prompt)).capitalize()
                        if lookUpLocation in quitOrback:
                            return lookUpLocation.lower()
                        employee_list = self.logicWrapper.listEmployees(location=lookUpLocation)  
                        prompt = 'Please choose a option from the given set of locations above\nPlease try again: '
                    returnValue = self.showEmployeesInfo(employee_list)
                    
            if returnValue == 'q':
                return 'q'

                    

    

    def showEmployeeID(self) -> str | bool:
        # use Search class there is Employee Search class there that can search by any param in this case kennitala
        employee = []
        prompt = 'Enter a kennitala'
        while not employee:
            lookUpKennitala = self.getValidInput("look for employee",prompt, validation.validateKennitala)
            if lookUpKennitala.lower() in quitOrback:
                return lookUpKennitala.lower()
            employee = self.logicWrapper.listEmployees(kennitala=lookUpKennitala)  # Call the wrapper that is
            prompt = 'This kennitala doesnt exist in the system\nPlease try again: '

        employee_list = [f'{key}: {value}' for key, value in list(employee[0].__dict__.items())[1:]]

        return self.takeInputAndPrintMenuWithoutBrackets(['[Q]uit', '[B]ack'], (f'List employees', employee_list, 'Choose a option: '))


    def showEmployeesInfo(self, employee_list: list[Employee]) -> str:
        if not employee_list:
            return self.takeInputAndPrintMenu(['[Q]uit', '[B]ack'], (f'List employees', '', 'No employees registered to this location\nChoose a option: '))

        body = []

        # Initialize column names
        headers = ['Name', 'Location', 'Phone number']

        # Calculate the maximum width for each column

        max_name_length = max(len(employee.name) for employee in employee_list)
        max_location_length = 12
        max_phone_length = 12


        # Build the line separator based on the column widths
        line = '+' + '-' * (max_name_length + 2) + '+' + '-' * (max_location_length + 2) + '+' + '-' * (max_phone_length + 2) + '+'

        # Build the header row
        header_row = f"| {headers[0]:<{max_name_length}} | {headers[1]:<{max_location_length}} | {headers[2]:<{max_phone_length}} |"

        # Append the header and line to body
        body.append(line)
        body.append(header_row)
        body.append(line)

        # Build each employee row
        for dict in employee_list:
            line_content = f"| {dict.name:<{max_name_length}} | {dict.location:<{max_location_length}} | {dict.phone:<{max_phone_length}} |"
            body.append(line_content)
            body.append(line)
    
    

        return self.takeInputAndPrintMenuWithoutBrackets(['[Q]uit', '[B]ack'], (f'List employees', body, 'Choose a option: '))
    



    def propertySearch(self) -> str:
                # use Search class there is Employee Search class there that can search by any param in this case kennitala
        userOption = self.takeInputAndPrintMenu( ['Location search', 'Property number search'], ('View property', ['Location search', 'Property number search'], "Choose a option: "))
        if userOption.lower() in quitOrback:
            return userOption.lower()
        match userOption.lower():
            case 'l':
                propertyList = []
                locations = self.logicWrapper.listLocations()
                prompt = 'Pick a location from the given options: '
                locationList = [location.airport for location in locations]
                while not propertyList:
                    lookUpLocation = self.takeInputAndPrintMenuWithoutBrackets('', ('Look up property by location', locationList, prompt)).capitalize()
                    if lookUpLocation.lower() in quitOrback:
                        return lookUpLocation.lower()
                    self.showPropertyInfo(self.logicWrapper.listProperties(location=lookUpLocation))
                    prompt = 'Please type in a location from the given options\nPick a location from the given options: '
            case 'p':
                returnValue = self.showropertyNumberSearch()
            
        if returnValue == 'q':
            return 'q'


    def showPropertyInfo(self, propertyList: list[Property], options: str = ['[Q]uit', '[B]ack'], prompt: str = 'Choose a option') -> str:

        # use Search class there is Employee Search class there that can search by any param in this case kennitala

        body = []

        # Initialize column names
        headers = ['Property ID', 'address', 'condition', 'Location']

        # Calculate the maximum width for each column
        try: 
            max_id_length = len('Property ID')
            max_address_length = max(len(employee.address) for employee in propertyList)
            max_address_length = max(len('address'), max_address_length)
            max_condition_length = 10
            max_location_length = 13
        except ValueError:
            return None


        # Build the line separator based on the column widths
        line = '+' + '-' * (max_id_length + 2) + '+' + '-' * (max_address_length + 2) + '+' + '-' * (max_condition_length + 2) + '+' + '-' * (max_location_length + 2) + '+'

        # Build the header row
        header_row = f"| {headers[0]:<{max_id_length}} | {headers[1]:<{max_address_length}} | {headers[2]:<{max_condition_length}} | {headers[3]:<{max_location_length}} |"

        # Append the header and line to body
        body.append(line)
        body.append(header_row)
        body.append(line)

        # Build each employee row
        for dict in propertyList:
            line_content = f"| {dict.id:<{max_id_length}} | {dict.address:<{max_address_length}} | {dict.condition:<{max_condition_length}} | {dict.location:<{max_condition_length}}    |"
            body.append(line_content)
            body.append(line)


        return self.takeInputAndPrintMenuWithoutBrackets(options, (f'List properties', body, prompt))
    

    def showropertyNumberSearch(self) -> str | bool:
        property = []
        prompt = "Enter property number: "
        while not property:
            lookUpLocation = self.getValidInput("look for property",prompt, validation.validateText)
            if lookUpLocation.lower() in quitOrback:
                return lookUpLocation.lower()
            property = self.logicWrapper.listProperties(id = lookUpLocation)  
            prompt = 'There is no property number assigned to the property you entered\nPlease try again: '
        propertyInstance = property[0]

        valueList = [f'Property number: {propertyInstance.id}', f'Location: {propertyInstance.location}',f'Address: {propertyInstance.address}', f'Condition: {propertyInstance.condition}',
                     f'Facilities requiring maintenance: {propertyInstance.facilitiesMaintenance}', f'Room count: {len(propertyInstance.rooms)}', f'Facility count: {len(propertyInstance.facilities)}']
    

        return self.takeInputAndPrintMenuWithoutBrackets(['[Q]uit', '[B]ack'], ('look for property', valueList, 'Choose a option: '))




    def workOrderSearch(self) -> str | bool:
        options = ['ID search', 'Property number search', 'Kennitala search']
        userOption = self.takeInputAndPrintMenu(options, ('Search work order', options, 'Choose a option:  '))
        if userOption.lower() in quitOrback:
            return userOption.lower()

        match userOption.lower():
            case 'i':
                workOrderID = None
                prompt = 'Choose a work order ID'
                while not workOrderID:
                    lookUpid = self.takeInputAndPrintMenuWithoutBrackets('', ('Search work order', ['Enter the ID of the work report you are looking for'], prompt, ''))
                    if lookUpid.lower() in quitOrback:
                        return lookUpid.lower()
                    workOrders = self.logicWrapper.listWorkOrders(id = lookUpid)
                    workOrderID = self.showWorkOrders(workOrders)
                    prompt = 'No work order exists with that ID\nPlease try again:  '
                workOrders = self.logicWrapper.listWorkOrders(id = lookUpid)  
                body = self.showWorkOrders(workOrders)
            case 'p':
                propertiesWorkOrders = ''
                prompt = 'Enter a property number: '
                while not propertiesWorkOrders:
                    lookUpPropertyNumber = self.takeInputAndPrintMenu([], ('Search Work orders','', prompt))
                    if lookUpPropertyNumber.lower() in quitOrback:
                        return lookUpPropertyNumber.lower()
                    workOrders = self.logicWrapper.listWorkOrders(propertyNumber = lookUpPropertyNumber)
                    propertiesWorkOrders = self.showWorkOrders(workOrders)
                    prompt = 'No work orders have been assinged to this property number\nEnter a property number: '
                workOrders = self.logicWrapper.listWorkOrders(propertyNumber = lookUpPropertyNumber)  
                body = self.showWorkOrders(workOrders)    

            case 'k':
                KennitalaWorkOrders = None
                prompt = 'Enter a kennitala: '
                while not KennitalaWorkOrders:
                    lookUpKennitala = self.takeInputAndPrintMenu([], ('Search Work orders','', prompt))
                    if lookUpKennitala.lower() in quitOrback:
                        return lookUpKennitala.lower()
                    KennitalaWorkOrders = self.logicWrapper.listWorkOrders(userID = lookUpKennitala)
                    body = self.showWorkOrders(KennitalaWorkOrders)
                    prompt = 'No employee with this kennitala has assigned a work order\nEnter a kennitala: '

               

        if body is None:
            return self.takeInputAndPrintMenuWithoutBrackets(['[Q]uit', '[B]ack'], ('Search work order', ['No work orders werer found'], 'Choose a option: ' ,''))


        return self.takeInputAndPrintMenuWithoutBrackets(['[Q]uit', '[B]ack'], ('Search work order', body, 'Choose a option: ' ,''))
            
    
    def showWorkOrders(self, workOrders: list[WorkOrder]) -> str:

        if not workOrders:
            return None

        body = []
        now = []
        asap = []
        emergency = []
        for instance in workOrders: # looping through every current work order
            propertyForWorkOrder = self.logicWrapper.listProperties(id = instance.propertyNumber)
            txt = ''
            txt += f'WORK ORDER #{instance.id}, Location {propertyForWorkOrder[0].location}\n'
            txt += f'       Priority: {instance.priority}\n'
            txt += f'       Description: {instance.description}\n'
            txt += f'       Property Number: {instance.propertyNumber}\n'
            if int(instance.contractorID) > -1:
                contractor = self.logicWrapper.listContractors(id = instance.contractorID)
                txt += f'       Contractor: {contractor[0].name}\n'
            else:
                txt += f'       Contractor: No contractor is assigned to this work order\n'
            if int(instance.userID) != 0:
                Employee = self.logicWrapper.listEmployees(kennitala = instance.userID)
                txt += f'       Employee: {Employee[0].name}\n'
            txt += f'       Room/facility: {instance.roomFacilityId}\n'
            txt += f'       Status:{' Not completed' if not instance.isCompleted else ' Completed'}\n\n'

            if instance.priority.lower() == 'now':
                now.append(txt)
            elif instance.priority.lower() == 'emergency':
                emergency.append(txt)
            else:
                asap.append(txt)
        
        body.extend(now)
        body.extend(asap)
        body.extend(emergency)
 
        return body



    def workReportSearch(self):
        userSelection = self.takeInputAndPrintMenu(['Propery search', 'Employee search'], ('Search work reports', ['Propery search', 'Employee search'], 'Choose a option'))
        if userSelection.lower() in quitOrback:
            return userSelection.lower()
        match userSelection.lower():
            case 'p':
                propertiesWorkReports = None
                prompt = 'Enter a property number: '
                while not propertiesWorkReports:
                    lookUpPropertyNumber = self.takeInputAndPrintMenu([], ('Search Work reports','', prompt))
                    if lookUpPropertyNumber.lower() in quitOrback:
                        return lookUpPropertyNumber.lower()
                    workReports = self.logicWrapper.listWorkReports(propertyNumber = lookUpPropertyNumber)
                    propertiesWorkReports = self.showWorkReports(workReports)
                    prompt = 'No work reports have been assinged to this property number\nEnter a property number: '
                workOrders = self.logicWrapper.listWorkReports(propertyNumber = lookUpPropertyNumber)  
                body = self.showWorkReports(workOrders)    

            case 'e':
                KennitalaWorkReports = None
                prompt = 'Enter a kennitala: '
                while not KennitalaWorkReports:
                    lookUpKennitala = self.takeInputAndPrintMenu([], ('Search Work reports','', prompt))
                    if lookUpKennitala.lower() in quitOrback:
                        return lookUpKennitala.lower()
                    KennitalaWorkReports = self.logicWrapper.listWorkReports(employeeID = lookUpKennitala)
                    body = self.showWorkReports(KennitalaWorkReports)
                    prompt = 'No employee with this kennitala has assigned a work report\nEnter a kennitala: '

        return self.takeInputAndPrintMenuWithoutBrackets([], ('Search work reports', body, 'Choose a option: '))

    def showWorkReports(self, workReports: list[WorkReport]) -> str:
        if not workReports:
            return None
        
        body = []

        for workreport in workReports:
            body.append(f'ID: {workreport.id}')
            body.append(f'Work order ID: {workreport.workOrderID}')
            body.append(f'description:  {workreport.description}')
            if int(workreport.contractorID) != -1:
                contractor = self.logicWrapper.listContractors(id = int(workreport.contractorID))
                body.append(f'Contractor:  {contractor[0].name}')
            else:
                body.append(f'Contractor: No contractor is assigned to this work report')
            employee = self.logicWrapper.listEmployees(kennitala = workreport.employeeID)
            body.append(f'Employee:  {employee[0].name}')
            body.append(f'Date: {workreport.date}')
            body.append(f'Total cost:  {workreport.cost}kr\n\n')
        

        return body
            





    def showContractorsInfo(self, options = 'choose a option', userOption = ['[Q]uit', '[B]ack']) -> str | bool:
        contractors = self.logicWrapper.listContractors()
        body = []

        # Initialize column names
        headers = ['Company name', 'Phone', 'Hours', 'Location', 'id']

        # Calculate the maximum width for each column
        max_name_length = max(len(contractor.name) for contractor in contractors)
        max_name_length = max(max_name_length, len('Company name'))

        max_phone_length = max(len(contractor.phone) for contractor in contractors)
        max_openingHours_length = max(len(contractor.openingHours) for contractor in contractors)
        max_location_length = 14
        max_id_length = 5



        # Build the line separator based on the column widths
        line = '+' + '-' * (max_name_length + 2) + '+' + '-' * (max_phone_length + 2) + '+' + '-' * (max_openingHours_length + 2) + '+' + '-' * (max_location_length) + '+' + '-' * (max_id_length) + '--+'


        # Build the header row
        header_row = f"| {headers[0]:<{max_name_length}} | {headers[1]:<{max_phone_length}} | {headers[2]:<{max_openingHours_length}} | {headers[3]:<{max_location_length - 2}} | {headers[4]:<{max_id_length}} |"

        # Append the header and line to body
        body.append(line)
        body.append(header_row)
        body.append(line)

        # Build each employee row
        for instance in contractors:
            line_content = f"| {instance.name:<{max_name_length}} | {instance.phone:<{max_phone_length}} | {instance.openingHours:<{max_openingHours_length}} | {instance.location:<{max_location_length - 2}} | {instance.id:<{max_id_length}} |"
            body.append(line_content)
            body.append(line)
    
    

        return self.takeInputAndPrintMenuWithoutBrackets(userOption, (f'List contractors', body, options))
