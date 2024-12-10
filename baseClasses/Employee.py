import json

class Employee:
    def __init__(self,kennitala: int = 0, name: str = "", phone: str = "", homePhone: str = "", address: str = "", email: str = "", location: str = '') -> None:
        self.kennitala: int = kennitala
        self.name: str = name
        self.phone: str = phone
        self.homePhone: str = homePhone
        self.address: str = address
        self.email: str = email
        self.location: str = location


    def __repr__(self) -> str:
        return f"Employee(kennitala={self.kennitala}, name={self.name}, phone={self.phone}, homePhone={self.homePhone}, address={self.address}, email={self.email}, location={self.location})"


    def normalize(self, jsonData: list[dict]) -> list['Employee']:
        employees: list['Employee'] = []
        for data in jsonData:

            employee: 'Employee' = Employee(**data)

            employees.append(employee)

        return employees


    def toJSON(self, employee: 'Employee') -> str:
        return json.dumps(employee.__dict__)
