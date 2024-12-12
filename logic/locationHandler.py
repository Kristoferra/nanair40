from baseClasses.Location import Location
from typing import Any


class LocationHandler:
    def __init__(self, dataWrapper=None) -> None:
        self.dataWrapper = dataWrapper
        self.location = Location()

    def addLocation(self, location: 'Location') -> bool:
        return self.dataWrapper.locationInsert(location)


    def editLocation(self, entry: str, entryValue: Any, **kwargs) -> bool:
        if not len(kwargs):
            return False
        if any(kwarg not in vars(self.location) for kwarg in kwargs):
            return False
        return self.dataWrapper.locationChange(entry, entryValue, **kwargs)


    def listLocations(self, **kwargs) -> list['Location']:
        if any(kwarg not in vars(self.location) for kwarg in kwargs):
            return []

        locations: list['Location'] = self.dataWrapper.locationFetch()
        if not len(kwargs):
            return locations

        for k, v in kwargs.items():
            # Top to bottom if we go bottom to top we get index out of range
            # Because things get deleted if they do not match the query before we loop through them if we go bottom to top
            for i in range(len(locations)-1, -1, -1):
                # hack around to check if result that might be int or float partialy contains our target number
                if str(v) != str(locations[i].__dict__[k]):
                    del locations[i]


        return locations
