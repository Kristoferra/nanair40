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
from logic.locationHandler import LocationHandler
from baseClasses.Location import Location
from dataControl.dataWrapper import DataWrapper
from typing import Any



class Logic_Wrapper:
    def __init__(self) -> None:
        self.dataWrapper = DataWrapper()
        self.employeeHandler = EmployeeHandler(self.dataWrapper)
        self.propertyHandler = PropertyHandler(self.dataWrapper)
        self.workOrderHandler = WorkOrderHandler(self.dataWrapper)
        self.workReportHandler = WorkReportHandler(self.dataWrapper)
        self.contractorHandler = ContractorHandler(self.dataWrapper)
        self.locationHandler = LocationHandler(self.dataWrapper)
        self.currentContractors: list['Contractor'] = self.contractorHandler.listContractors()
        if len(self.currentContractors):
            self.currentContractorID: int = int(self.currentContractors[-1].id)
        else:
            self.currentContractorID = 1
        self.currentWorkOrders: list['WorkOrder'] = self.workOrderHandler.listWorkOrders()
        if len(self.currentWorkOrders):
            self.currentWorkOrderID: int = int(self.currentWorkOrders[-1].id)
        else:
            self.currentWorkOrderID = 1



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
        self.currentWorkOrderID+=1
        return self.workOrderHandler.addWorkOrder(work)

    def editWorkOrder(self, entry: str, entryValue: Any, **kwargs) -> bool:
        return self.workOrderHandler.editWorkOrder(entry, entryValue, **kwargs)

    def listWorkOrders(self, **kwargs) -> list['WorkOrder']:
        return self.workOrderHandler.listWorkOrders(**kwargs)
    
    def listWorkCurrentWorkOrders(self, **kwargs) -> list['WorkOrder']:
        return self.workOrderHandler.listWorkCurrentOrders(**kwargs)
    
    def addWorkReport(self, workReport: 'WorkReport') -> bool:
        return self.workReportHandler.addWorkReport(workReport)
    def currentWorkReportID(self) -> int:
        return self.workReportHandler.currentWorkReportID()

    def listWorkOrders(self, **kwargs) -> list[WorkOrder]:

        return self.workOrderHandler.listWorkOrders(**kwargs)

    def addContractor(self, contractor: 'Contractor') -> bool:
        self.currentContractorID+=1
        return self.contractorHandler.addContractor(contractor)

    def editContractor(self, entry: str, entryValue: Any, **kwargs) -> bool:
        return self.contractorHandler.editContractor(entry, entryValue, **kwargs)

    def listContractors(self, **kwargs) -> list['Contractor']:
        return self.contractorHandler.listContractors(**kwargs)
    
    def listLocations(self, **kwargs) -> list[Location]:
        return self.locationHandler.listLocations(**kwargs)

    def checkRepeatingWorkOrders(self, **kwargs) -> bool:
        return self.workOrderHandler.checkRepeatingWorkOrders(**kwargs)

    def listWorkReports(self, **kwargs) -> list[WorkReport]:
        return self.workReportHandler.listWorkReports(**kwargs)

    def editWorkOrder(self, entry: str, entryValue: Any, **kwargs) -> bool:
        return self.workOrderHandler.editWorkOrder(entry, entryValue, **kwargs)
    
    def editWorkReports(self, entry: str, entryValue: Any, **kwargs) -> bool:
        return self.workReportHandler.editWorkReport(entry, entryValue, **kwargs)
