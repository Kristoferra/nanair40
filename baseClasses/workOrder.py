import json
from baseClasses.workReport import WorkReport

"""
ADD REPEATING WORK ORDERS
"""
class WorkOrder:
    def __init__(self, id: int = 0, date: str = "", description: str = "", propertyNumber: str = "", userID: int = 0, priority: str = "", workReport: list['WorkReport'] = [], contractorID: int = 0, isCompleted: bool = False, roomFacilityId: int = 0, sentToManager: bool = False, repeating: bool = False, repeatInterval: int = 0):
        self.id: int = id
        self.date: str = date
        self.description: str = description
        self.propertyNumber: str = propertyNumber
        self.userID: int = userID
        self.priority: str = priority
        self.workReport: list['WorkReport'] = workReport
        self.contractorID: int = contractorID # if it is -1 it is nobody if it is > -1 then it is an actual contrator
        self.sentToManager: bool = sentToManager
        self.isCompleted: bool = isCompleted
        self.roomFacilityId: int = roomFacilityId
        self.repeating: bool = repeating
        self.repeatInterval: int = repeatInterval


    def __repr__(self) -> str:
        return f"WorkOrder(id={self.id}, date={self.date}, description={self.description}, propertyNumber={self.propertyNumber}, userID={self.userID}, priority={self.priority}, contractorID={self.contractorID}, isCompleted={self.isCompleted}, repeating={self.repeating}, repeatInterval={self.repeatInterval})"


    def normalize(self, jsonData: list[str]) -> list['WorkOrder']:
        workOrders: list['WorkOrder'] = []
        for data in jsonData:

            workOrder: 'WorkOrder' = WorkOrder(**data)

            workOrders.append(workOrder)

        return workOrders

    def toJSON(self, workOrder: 'WorkOrder') -> str:
        return json.dumps(workOrder.__dict__)
