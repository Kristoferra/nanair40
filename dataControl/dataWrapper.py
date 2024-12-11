from dataControl.contractorController import ContractorController
from dataControl.employeeController import EmployeeController
from dataControl.locationController import LocationController
from dataControl.propertyController import PropertyController
from dataControl.workOrderController import WorkController
from dataControl.workReportController import WorkReportController
from typing import Any


class DataWrapper:
    def __init__(self) -> None:
        self.employeeController = EmployeeController()
        self.propertyController = PropertyController()
        self.workOrderController = WorkController()
        self.workReportController = WorkReportController()
        self.contractorController = ContractorController()
        self.locationController = LocationController()


    def employeeInsert(self, data) -> bool:
        return self.employeeController.appendIntoFile(data)

    def employeeChange(self, entry: str, entryValue: Any, **kwargs) -> bool:
        return self.employeeController.changeOneEntry(entry, entryValue, **kwargs)

    def employeeFetch(self):
        return self.employeeController.readFile()

    def propertyFetch(self):
        return self.propertyController.readFile()

    def propertyChange(self, entry: str, entryValue: Any, **kwargs) -> bool:
        return self.propertyController.changeOneEntry(entry, entryValue, **kwargs)

    def propertyInsert(self, data) -> bool:
        return self.propertyController.appendIntoFile(data)

    def workOrderFetch(self):
        return self.workOrderController.readFile()

    def workOrderInsert(self, data) -> bool:
        return self.workOrderController.appendIntoFile(data)

    def workOrderChange(self, entry: str, entryValue: Any, **kwargs) -> bool:
        return self.workOrderController.changeOneEntry(entry, entryValue, **kwargs)

    def workReportInsert(self, data) -> bool:
        return self.workReportController.appendIntoFile(data)

    def workReportChange(self, entry: str, entryValue: Any, **kwargs) -> bool:
        return self.workReportController.changeOneEntry(entry, entryValue, **kwargs)

    def workReportFetch(self):
        return self.workReportController.readFile()

    def contractorFetch(self):
        return self.contractorController.readFile()

    def contractorInsert(self, data) -> bool:
        return self.contractorController.appendIntoFile(data)

    def contractorChange(self, entry: str, entryValue: Any, **kwargs) -> bool:
        return self.contractorController.changeOneEntry(entry, entryValue, **kwargs)

    def locationFetch(self):
        return self.locationController.readFile()

    def locationInsert(self, data) -> bool:
        return self.locationController.appendIntoFile(data)

    def locationChange(self, entry: str, entryValue: Any, **kwargs) -> bool:
        return self.locationController.changeOneEntry(entry, entryValue, **kwargs)
