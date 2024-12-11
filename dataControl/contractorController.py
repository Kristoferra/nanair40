import json
import os
import tempfile
from typing import Any

from baseClasses.Contractor import Contractor

def atomicWrite(fp, data):
    dirName = os.path.dirname(fp)
    with tempfile.NamedTemporaryFile("w", delete=False, dir=dirName) as tmpFile:
        json.dump(data, tmpFile, indent=4)
        tmpFileName = tmpFile.name
        tmpFile.flush()
        os.fsync(tmpFile.fileno()) # if you cut off the power of kernel panics

    os.replace(tmpFileName, fp)



class ContractorController:
    def __init__(self):
        self.contractor = Contractor()
        self.filePath = "data/contractors.json"


    def appendIntoFile(self, data: 'Contractor') -> bool:
        try:
            with open(self.filePath, "r") as f:
                currentData = json.load(f)
        except:
            currentData = []
        try:
            dataJSON = self.contractor.toJSON(data)
            currentData.append(json.loads(dataJSON))

            atomicWrite(self.filePath, currentData)
            return True
        except:
            return False

    # We typehint any for value cuz some of them are str, some int, some bool
    def changeOneEntry(self, entry: str, entryValue: Any, **kwargs) -> bool:
        try:
            with open(self.filePath, "r") as f:
                currentData = json.load(f)
        except:
            currentData = []
        try:
            for contractor in currentData:
                if contractor.get(entry) == entryValue:
                    for key, value in kwargs.items():
                        if key in contractor:
                            contractor[key] = value
                    break
            else:
                return False

            atomicWrite(self.filePath, currentData)
            return True
        except:
            return False


    def readFile(self) -> list['Contractor']:
        try:
            data = []
            with open(self.filePath, "r") as f:
                data = json.load(f)
            return self.contractor.normalize(data)
        except:
            return []
