"""
fix to camelCase not python_case
"""

from logic.employeeHandler import EmployeeHandler
from baseClasses.Employee import Employee
from logic.PropertyHandler import PropertyHandler
from baseClasses.Property import Property
from logic.workOrderHandler import WorkOrderHandler
from logic.workReportHandler import WorkReportHandler
from baseClasses.workReport import WorkReport
from baseClasses.workOrder import WorkOrder
from logic.contractorHandler import ContractorHandler
from baseClasses.Contractor import Contractor
from typing import Any

class Logic_Wrapper:
    def __init__(self) -> None:
        self.employeeHandler = EmployeeHandler()
        self.propertyHandler = PropertyHandler()
        self.workOrderHandler = WorkOrderHandler()
        self.workReportHandler = WorkReportHandler()
        self.contractorHandler = ContractorHandler()

    def addEmployee(self, employee: Employee) -> bool:
        return self.employeeHandler.addEmployee(employee)
    
    def editEmployee(self, entry: str, entryValue: Any, **kwargs) -> bool:
        return self.employeeHandler.editEmployee(entry, entryValue, **kwargs)
    
    def listEmployees(self, **kwargs) -> list['Employee']:
        return self.employeeHandler.listEmployes(**kwargs)

    def addProperty(self, property: Property) -> bool:
        return self.propertyHandler.addProperty(property)
    
    def listProperties(self, **kwargs) -> list['Property']:
        return self.propertyHandler.listProperties(**kwargs)
    
    def editProperty(self, entry: str, entryValue: Any, **kwargs) -> bool:
        return self.propertyHandler.editProperty(entry, entryValue, **kwargs)

    def addWorkOrder(self, work: 'WorkOrder') -> bool:
        return self.workOrderHandler.addWorkOrder(work)

    def editWorkOrder(self, entry: str, entryValue: Any, **kwargs) -> bool:
        return self.workOrderHandler.editWorkOrder(entry, entryValue, **kwargs)

    def listWorkOrders(self, **kwargs) -> list['WorkOrder']:
        return self.workOrderHandler.listWorkOrders(**kwargs)
    
    def addWorkReport(self, workReport: 'WorkReport') -> bool:
        return self.workReportHandler.addWorkReport(workReport)

    def editWorkOrder(self, workReportID: str, **kwargs) -> bool:
        return self.workReportHandler.editWorkReport(workReportID, **kwargs)

    def listWorkOrders(self, **kwargs) -> list['WorkReport']:
        return self.workOrderHandler.listWorkOrders(**kwargs)

    def addContractor(self, contractor: 'Contractor') -> bool:
        return self.contractorHandler.addContractor(contractor)

    def editContractor(self, entry: str, entryValue: Any, **kwargs) -> bool:
        return self.contractorHandler.editContractor(entry, entryValue, **kwargs)

    def listContractors(self, **kwargs) -> list['Contractor']:
        return self.contractorHandler.listContractors(**kwargs)
