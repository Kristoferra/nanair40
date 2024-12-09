import json
from baseClasses.workReport import WorkReport

"""
ADD REPEATING WORK ORDERS
"""
class WorkOrder:
    def __init__(self, id: int = 0, date: str = "", description: str = "", propertyNumber: int = 0, userID: int = 0, priority: int = 0, workReport: list['WorkReport'] = [], contractorID: int = 0, isCompleted: bool = False, roomFacilityId: int = 0):
        self.id: int = id
        self.date: str = date
        self.description: str = description
        self.propertyNumber: int = propertyNumber
        self.userID: int = userID
        self.priority: int = priority # 0 1 2
        self.workReport: list['WorkReport'] = workReport
        self.contractorID: int = contractorID # if it is -1 it is nobody if it is > -1 then it is an actual contrator
        self.isCompleted: bool = isCompleted
        self.roomFacilityId: int = roomFacilityId


    def __repr__(self) -> str:
        return f"WorkOrder(id={self.id}, date={self.date}, description={self.description}, propertyNumber={self.propertyNumber}, userID={self.userID}, priority={self.priority}, contractorID={self.contractorID}, isCompleted={self.isCompleted})"


    def normalize(self, jsonData: list[str]) -> list['WorkOrder']:
        workOrders: list['WorkOrder'] = []
        for data in jsonData:

            workOrder: 'WorkOrder' = WorkOrder(**data)

            workOrders.append(workOrder)

        return workOrders

    def toJSON(self, workOrder: 'WorkOrder') -> str:
        return json.dumps(workOrder.__dict__)
