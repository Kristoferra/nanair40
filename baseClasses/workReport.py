import json


class WorkReport:
    def __init__(self, id: int = 0, workOrderID: int = 0, description: str = "", contractorID: int = 0, date: str = "", cost: int = 0, comment: str = ""):
        self.id: int = id
        self.workOrderID: int = workOrderID
        self.description: str = description
        self.contractorID: int = contractorID
        self.date: str = date
        self.cost: int = cost
        self.comment: str = comment


    def __repr__(self) -> str:
        return f"WorkReport(id={self.id}, workOrderID={self.workOrderID}, description={self.description}, date={self.date}, cost={self.cost}, comment={self.comment})"


    def normalize(self, jsonData: list[str]) -> list['WorkReport']:
        workreports: list['WorkReport'] = []
        for data in jsonData:
            workreport: 'WorkReport' = WorkReport(**data)

            workreports.append(workreport)

        return workreports


    def toJSON(self, workreport: 'WorkReport') -> str:
        return json.dumps(workreport.__dict__)
