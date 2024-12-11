import json

class Location:
    def __init__(self, country: str = "", airport: str = "", phone: str = "", openingHours: str = "", operationsManagerID: int = 0) -> None:
        self.country: str = country # The locations country
        self.airport: str = airport # The locations airport
        self.phone: str = phone # The locations phone
        self.openingHours: str = openingHours # The locations opening hours
        self.operationsManagerID: int = operationsManagerID # The locations manager ID

    # String representation of the Employee object, needed for JSON handling
    def __repr__(self) -> str:
        return f"Location(country={self.country}, airport={self.airport}, phone={self.phone}, openingHours={self.openingHours}, operationsManagerID={self.operationsManagerID})"

    # Method to normalize a list of locations data (represented as dictionaries) into Locations objects
    def normalize(self, jsonData: list[dict]) -> list['Location']:
        locations: list['Location'] = []
        for data in jsonData:

            location: 'Location' = Location(**data)

            locations.append(location)

        return locations

    # Method to convert an locations object to a JSON string (serialization)
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
