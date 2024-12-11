import json
import os
import tempfile
from typing import Any

from baseClasses.Employee import Employee

def atomicWrite(fp, data):
    dirName = os.path.dirname(fp)
    with tempfile.NamedTemporaryFile("w", delete=False, dir=dirName) as tmpFile:
        json.dump(data, tmpFile, indent=4)
        tmpFileName = tmpFile.name
        tmpFile.flush()
        os.fsync(tmpFile.fileno()) # if you cut off the power of kernel panics

    os.replace(tmpFileName, fp)



class EmployeeController:
    def __init__(self):
        self.employee = Employee()
        self.filePath = "data/employees.json"


    def appendIntoFile(self, data: 'Employee') -> bool:
        try:
            with open(self.filePath, "r") as f:
                currentData = json.load(f)
        except:
            currentData = []
        try:
            dataJSON = self.employee.toJSON(data)
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
            for employee in currentData:
                if employee.get(entry) == entryValue:
                    for key, value in kwargs.items():
                        if key in employee:
                            employee[key] = value
                    break
            else:
                return False

            atomicWrite(self.filePath, currentData)
            return True
        except:
            return False


    def readFile(self) -> list['Employee']:
        try:
            data = []
            with open(self.filePath, "r") as f:
                data = json.load(f)
            return self.employee.normalize(data)
        except:
            return []
