import json

class Contractor:
    def __init__(self, id: int = 0, name: str = "", phone: str = "", openingHours: str = "", location: int = 0) -> None:
        self.id: int = id # Contractors ID
        self.name: str = name # Contractors name
        self.phone: str = phone # Contractors phone
        self.openingHours: str = openingHours # might change to dae
        self.location: int = location # Contractors location

    # String format for handling Contractor 
    def __repr__(self) -> str:
        return f"Contractor(id={self.id}, name={self.name}, phone={self.phone}, openingHours={self.openingHours}, location={self.location})"

    # Method to normalize a list of contractor data (represented as dictionaries) into Contractors objects
    def normalize(self, jsonData: list[str]) -> list['Contractor']:
        contractors: list['Contractor'] = []
        for data in jsonData:

            contractor: 'Contractor' = Contractor(**data)

            contractors.append(contractor)

        return contractors

    # Method to convert an Contractors object to a JSON string (serialization)
    def toJSON(self, contractor: 'Contractor') -> str:
        return json.dumps(contractor.__dict__)
