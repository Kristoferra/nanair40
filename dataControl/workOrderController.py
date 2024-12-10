import json
import os
import tempfile
from typing import Any

from baseClasses.workOrder import WorkOrder

def atomicWrite(fp, data):
    dirName = os.path.dirname(fp)
    with tempfile.NamedTemporaryFile("w", delete=False, dir=dirName) as tmpFile:
        json.dump(data, tmpFile, indent=4)
        tmpFileName = tmpFile.name
        tmpFile.flush()
        os.fsync(tmpFile.fileno()) # if you cut off the power of kernel panics

    os.replace(tmpFileName, fp)



class WorkController:
    def __init__(self):
        self.workOrder = WorkOrder()
        self.filePath = "data/workOrders.json"


    def appendIntoFile(self, data: 'WorkOrder') -> bool:
        try:
            with open(self.filePath, "r") as f:
                currentData = json.load(f)
        except:
            currentData = []

        try:
            dataJSON = self.workOrder.toJSON(data)
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

            for workOrder in currentData:
                if workOrder.get(entry) == entryValue:
                    for key, value in kwargs.items():
                        if key in workOrder:
                            workOrder[key] = value
                    break
            else:
                return False

            atomicWrite(self.filePath, currentData)
            return True
        except:
            return False


    def readFile(self) -> list['WorkOrder']:
        data = []
        with open(self.filePath, "r") as f:
            data = json.load(f)
        return self.workOrder.normalize(data) 