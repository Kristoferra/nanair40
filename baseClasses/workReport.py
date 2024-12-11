import json


class WorkReport:
    def __init__(self, id: int = 0, workOrderID: int = 0, description: str = "", contractorID: int = 0, employeeID: int = 0, date: str = "", cost: int = 0, comment: str = "", isCompleted: bool = False):
        self.id: int = id # Work report ID
        self.workOrderID: int = workOrderID # The work order ID the report is about
        self.description: str = description # Contents of the work report
        self.contractorID: int = contractorID # Work report's contractor ID
        self.employeeID: int = employeeID # Work report's employee ID
        self.date: str = date # Work report date
        self.cost: int = cost # work report cost
        self.comment: str = comment # comment that a manager has made for the work report
        self.isCompleted: bool = isCompleted # Work report value to see if the work is done: True=done, False=not done

    # String representation of the Work report object, needed for JSON handling
    def __repr__(self) -> str:
        return f"WorkReport(id={self.id}, workOrderID={self.workOrderID}, employeeID={self.employeeID}, description={self.description}, date={self.date}, cost={self.cost}, comment={self.comment}, isCompleted={self.isCompleted})"

    # Method to normalize a list of Work report data (represented as dictionaries) into work report objects
    def normalize(self, jsonData: list[str]) -> list['WorkReport']:
        workreports: list['WorkReport'] = []
        for data in jsonData:
            workreport: 'WorkReport' = WorkReport(**data)

            workreports.append(workreport)

        return workreports

    # Method to convert an work report object to a JSON string (serialization)
    def toJSON(self, workreport: 'WorkReport') -> str:
        return json.dumps(workreport.__dict__)
