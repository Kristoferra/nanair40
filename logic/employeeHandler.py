from baseClasses.Employee import Employee
from typing import Any


class EmployeeHandler:
    def __init__(self, dataWrapper=None) -> None:
        self.dataWrapper = dataWrapper
        self.employee = Employee()

    def addEmployee(self, employee: 'Employee') -> bool:
        # https://www.quora.com/What-is-maximum-and-minimum-length-of-any-mobile-number-across-the-world
        # logic layer checking, here the data is confirmed to be true from UI layer, if not false is returned
        if not type(employee.kennitala) == str:
            return False
        if not employee.kennitala.isdigit():
            return False
        if len(str(employee.kennitala)) != 10:
            return False
        if self.listEmployes(kennitala=employee.kennitala):
            return False
        phoneWhitelist = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+"]
        if type(employee.phone) != str:
            return False
        if len(employee.phone) < 7 or len(employee.phone) > 15:
            return False
        cnt = 0
        for i in employee.phone:
            if i == "+":
                cnt+=1
            if cnt >= 2:
                return False
            if i not in phoneWhitelist:
                return False
        if type(employee.homePhone) != str:
            return False
        if len(employee.homePhone) < 7 or len(employee.homePhone) > 15:
            return False
        cnt = 0
        for i in employee.homePhone:
            if i == "+":
                cnt+=1
            if cnt >= 2:
                return False
            if i not in phoneWhitelist:
                return False

        return self.dataWrapper.employeeInsert(employee)


    def editEmployee(self, entry: str, entryValue: Any, **kwargs) -> bool:
        if not len(kwargs):
            return False
        if any(kwarg not in vars(self.employee) for kwarg in kwargs):
            return False
        # https://www.quora.com/What-is-maximum-and-minimum-length-of-any-mobile-number-across-the-world
        if entry == "kennitala":
            if not entryValue.isdigit():
                return False
            if len(str(entryValue)) != 10:
                return False
            if not self.listEmployes(kennitala=entryValue):
                return False
        if entry == "phone":
            if type(entryValue) != str:
                return False
            if len(entryValue) < 7 or len(entryValue) > 15:
                return False
        phoneWhitelist = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+"]
        cnt = 0
        for i in entryValue:
            if i == "+":
                cnt+=1
            if cnt >= 2:
                return False
            if i not in phoneWhitelist:
                return False
        
        if entry == "homePhone":
            if type(entryValue) != str:
                return False
            if len(entryValue) < 7 or len(entryValue) > 15:
                return False
        cnt = 0
        for i in entryValue:
            if i == "+":
                cnt+=1
            if cnt >= 2:
                return False
            if i not in phoneWhitelist:
                return False

        return self.dataWrapper.employeeChange(entry, entryValue, **kwargs)


    def listEmployes(self, **kwargs) -> list['Employee']:
        if any(kwarg not in vars(self.employee) for kwarg in kwargs):
            return []

        employees: list['Employee'] = self.dataWrapper.employeeFetch()
        if not len(kwargs):
            return employees

        for k, v in kwargs.items():
            # Top to bottom if we go bottom to top we get index out of range
            # Because things get deleted if they do not match the query before we loop through them if we go bottom to top
            for i in range(len(employees)-1, -1, -1):
                # hack around to check if result that might be int or float partialy contains our target number
                if str(v) != str(employees[i].__dict__[k]): # used to be not in but we only want exact matches so
                    del employees[i]


        return employees
