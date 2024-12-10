from baseClasses.workOrder import WorkOrder
from dataControl.workOrderController import WorkController
from typing import Any
from datetime import datetime
from dateutil.relativedelta import relativedelta

def time_diff_category(date1_str, date2_str):
    # Define the date format
    date_format = "%d.%m.%Y"
    
    # Parse the date strings into datetime objects
    date1 = datetime.strptime(date1_str, date_format)
    date2 = datetime.strptime(date2_str, date_format)
    
    # Calculate the absolute difference
    delta = relativedelta(date2, date1)
    
    # Check the difference and return appropriate category
    if delta.years > 0:
        return 4  # Year
    elif delta.months > 0:
        return 3  # Month
    elif delta.days > 7:
        return 2  # Week
    else:
        return 1  # Day



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


    def listRepeatingWorkOrders(self, **kwargs) -> list[WorkOrder]:
        repeatingList: list[WorkOrder] = self.listWorkOrders(repeating=True)

        currentDate = datetime.now()
        currentDate = currentDate.strftime("%d.%m.%Y")

        final = []
        for workOrder in repeatingList:
            if not workOrder.date:
                continue
            if not workOrder.isCompleted:
                final.append(workOrder)
                continue
            tdif = time_diff_category(workOrder.workReport[-1].date, currentDate)
            if tdif >= workOrder.repeatInterval:
                self.workOrderControl.changeOneEntry("id", workOrder.id, isCompleted=False)
                final.append(workOrder)
        return final
