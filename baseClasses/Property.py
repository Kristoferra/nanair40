import json

class Property:
    def __init__(self, id: int = 0, location: int = 0, address: str = "", condition: int = 0, facilitiesMaintenance: str = '', rooms: dict = {}, facilities: dict = {}) -> None:
        self.id: int = id # Property ID
        self.location: int = location # Property location
        self.address: str = address # The properties address
        self.condition: int = condition # 0 to 10 average calculation
        self.facilitiesMaintenance: str = facilitiesMaintenance # What maintenance the property needs
        self.rooms: dict = rooms # What rooms the property has
        self.facilities: dict = facilities # The facilities the property has



    # String representation of the Property object, needed for JSON handling
    def __repr__(self) -> str:
        return f"Property(id={self.id}, location={self.location}, address={self.address}, condition={self.condition}, facilities={self.facilities})"

    # Method to normalize a list of property data (represented as dictionaries) into property objects
    def normalize(self, jsonData: list[str]) -> list['Property']:
        properties: list['Property'] = []
        for data in jsonData:

            property: 'Property' = Property(**data)

            properties.append(property)

        return properties

    # Method to convert an property object to a JSON string (serialization)
    def toJSON(self, property: 'Property') -> str:
        return json.dumps(property.__dict__)
