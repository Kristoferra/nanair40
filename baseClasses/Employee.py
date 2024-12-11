import json

class Employee:
    def __init__(self,kennitala: int = 0, name: str = "", phone: str = "", homePhone: str = "", address: str = "", email: str = "", location: str = '') -> None:
        self.kennitala: int = kennitala # Employee's SSN used as ID in our code
        self.name: str = name # Employee's full name
        self.phone: str = phone # Employee's phone number
        self.homePhone: str = homePhone # Employee's home phone number
        self.address: str = address # Employee's address
        self.email: str = email # Employee's email address
        self.location: str = location # Employee's location


    # String representation of the Employee object, needed for JSON handling
    def __repr__(self) -> str:
        return f"Employee(kennitala={self.kennitala}, name={self.name}, phone={self.phone}, homePhone={self.homePhone}, address={self.address}, email={self.email}, location={self.location})"


    # Method to normalize a list of employee data (represented as dictionaries) into Employee objects
    def normalize(self, jsonData: list[dict]) -> list['Employee']:
        employees: list['Employee'] = []
        for data in jsonData:

            employee: 'Employee' = Employee(**data)

            employees.append(employee)

        return employees


    # Method to convert an Employee object to a JSON string (serialization)
    def toJSON(self, employee: 'Employee') -> str:
        return json.dumps(employee.__dict__)
