from baseClasses.Contractor import Contractor
from typing import Any


class ContractorHandler:
    def __init__(self, dataWrapper=None) -> None:
        self.dataWrapper = dataWrapper
        self.contractor = Contractor()

    def addContractor(self, contractor: 'Contractor') -> bool:
        return self.dataWrapper.contractorInsert(contractor)


    def editContractor(self, entry: str, entryValue: Any, **kwargs) -> bool:
        if not len(kwargs):
            return False
        if any(kwarg not in vars(self.contractor) for kwarg in kwargs):
            return False
        return self.dataWrapper.contractorChange(entry, entryValue, **kwargs)


    def listContractors(self, **kwargs) -> list['Contractor']:
        if any(kwarg not in vars(self.contractor) for kwarg in kwargs):
            return []

        contractors: list['Contractor'] = self.dataWrapper.contractorFetch()
        if not len(kwargs):
            return contractors

        for k, v in kwargs.items():
            # Top to bottom if we go bottom to top we get index out of range
            # Because things get deleted if they do not match the query before we loop through them if we go bottom to top
            for i in range(len(contractors)-1, -1, -1):
                # hack around to check if result that might be int or float partialy contains our target number
                if str(v) not in str(contractors[i].__dict__[k]):
                    del contractors[i]


        return contractors
