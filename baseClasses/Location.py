import json

class Location:
    def __init__(self, country: str = "", airport: str = "", phone: str = "", openingHours: str = "", operationsManagerID: int = 0) -> None:
        self.country: str = country
        self.airport: str = airport
        self.phone: str = phone
        self.openingHours: str = openingHours
        self.operationsManagerID: int = operationsManagerID

    def __repr__(self) -> str:
        return f"Location(country={self.country}, airport={self.airport}, phone={self.phone}, openingHours={self.openingHours}, operationsManagerID={self.operationsManagerID})"


    def normalize(self, jsonData: list[dict]) -> list['Location']:
        locations: list['Location'] = []
        for data in jsonData:

            location: 'Location' = Location(**data)

            locations.append(location)

        return locations


    def toJSON(self, location: 'Location') -> str:
        return json.dumps(location.__dict__)


"""
locations: dict = {'Iceland': ['Reykjavík'],
                   'Greenland': ['Nuuk', 'Kulusuk'],
                   'Faroe Islands': ['Tórshavn'],
                   'Shetland Islands': ['Tingwall'],
                   'Svalbard': ['Longyearbyen']
}
"""
