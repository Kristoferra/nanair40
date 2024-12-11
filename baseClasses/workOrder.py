import json
from baseClasses.workReport import WorkReport

"""
ADD REPEATING WORK ORDERS
"""
class WorkOrder:
    def __init__(self, id: int = 0, date: str = "", description: str = "", propertyNumber: str = "", userID: int = 0, priority: str = "", workReport: list['WorkReport'] = [], contractorID: int = 0, isCompleted: bool = False, roomFacilityId: int = 0, sentToManager: bool = False, repeating: bool = False, repeatInterval: int = 0):
        self.id: int = id # Work order ID
        self.date: str = date # Work order date
        self.description: str = description # The description for the work order
        self.propertyNumber: str = propertyNumber # The work orders property number
        self.userID: int = userID # The user ID attached to the work order
        self.priority: str = priority # Work order priority
        self.workReport: list['WorkReport'] = workReport # The work report for the work order(can be added later)
        self.contractorID: int = contractorID # if it is -1 it is nobody if it is > -1 then it is an actual contrator
        self.sentToManager: bool = sentToManager
        self.isCompleted: bool = isCompleted # Work order value to see if the work is done: True=done, False=not done
        self.roomFacilityId: int = roomFacilityId # The room ID for the work order
        self.repeating: bool = repeating # The value if its repeating "[D]aily, [W]eekly, [M]onthly, [Y]early"
        self.repeatInterval: int = repeatInterval

    # String representation of the Work order object, needed for JSON handling
    def __repr__(self) -> str:
        return f"WorkOrder(id={self.id}, date={self.date}, description={self.description}, propertyNumber={self.propertyNumber}, userID={self.userID}, priority={self.priority}, contractorID={self.contractorID}, isCompleted={self.isCompleted}, repeating={self.repeating}, repeatInterval={self.repeatInterval})"

    # Method to normalize a list of Work order data (represented as dictionaries) into work order objects
    def normalize(self, jsonData: list[str]) -> list['WorkOrder']:
        workOrders: list['WorkOrder'] = []
        for data in jsonData:

            workOrder: 'WorkOrder' = WorkOrder(**data)

            workOrders.append(workOrder)

        return workOrders

    # Method to convert an work order object to a JSON string (serialization)
    def toJSON(self, workOrder: 'WorkOrder') -> str:
        return json.dumps(workOrder.__dict__)
