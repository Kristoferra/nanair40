from baseClasses.workOrder import WorkOrder
from dataControl.workOrderController import WorkController
from typing import Any


class WorkOrderHandler:
    def __init__(self) -> None:
        self.workOrderControl = WorkController()
        self.workOrder = WorkOrder()

    def addWorkOrder(self, workOrder: 'WorkOrder') -> bool:
        return self.workOrderControl.appendIntoFile(workOrder)

    def editWorkOrder(self, entry: str, entryValue: Any, **kwargs) -> bool:
        if not len(kwargs):
            return False
        if any(kwarg not in vars(self.workOrder) for kwarg in kwargs):
            return False
        
        return self.workOrderControl.changeOneEntry(entry, entryValue, **kwargs)


    def listWorkOrders(self, **kwargs) -> list['WorkOrder']:
        if any(kwarg not in vars(self.workOrder) for kwarg in kwargs):
            return []

        workOrder: list['WorkOrder'] = self.workOrderControl.readFile()
        if not len(kwargs):
            return workOrder

        for k, v in kwargs.items():
            # Top to bottom if we go bottom to top we get index out of range
            # Because things get deleted if they do not match the query before we loop through them if we go bottom to top
            for i in range(len(workOrder)-1, -1, -1):
                # hack around to check if result that might be int or float partialy contains our target number
                if str(v) != str(workOrder[i].__dict__[k]):
                    del workOrder[i]

    # LIST workOrder REPORTS MAYBE


        return workOrder
    
    def listWorkCurrentOrders(self, **kwargs) -> list['WorkOrder']:
        if any(kwarg not in vars(self.workOrder) for kwarg in kwargs):
            return []

        workOrder: list['WorkOrder'] = self.workOrderControl.readFile()
        if not len(kwargs):
            return workOrder

        for k, v in kwargs.items():
            # Top to bottom if we go bottom to top we get index out of range
            # Because things get deleted if they do not match the query before we loop through them if we go bottom to top
            for i in range(len(workOrder)-1, -1, -1):
                # hack around to check if result that might be int or float partialy contains our target number
                if str(v) != str(workOrder[i].__dict__[k]):
                    del workOrder[i]

        for index, instance in enumerate(workOrder):
            if int(instance.userID) == 0:
                del workOrder[index]


        return workOrder
