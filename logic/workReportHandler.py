from baseClasses.workReport import WorkReport
from dataControl.workReportController import WorkReportController
from typing import Any
from datetime import datetime

def is_date_in_range(check_date_str, start_date_str, end_date_str):
    check_date = datetime.strptime(check_date_str, "%d-%m-%Y")
    start_date = datetime.strptime(start_date_str, "%d-%m-%Y")
    end_date = datetime.strptime(end_date_str, "%d-%m-%Y")
    
    return start_date <= check_date <= end_date



class WorkReportHandler:
    def __init__(self) -> None:
        self.workReportControl = WorkReportController()
        self.workReport = WorkReport()

    def addWorkReport(self, work: 'WorkReport') -> bool:
        return self.workReportControl.appendIntoFile(work)

    def editWorkReport(self, entry: str, entryValue: Any, **kwargs) -> bool:
        if not len(kwargs):
            return False
        if any(kwarg not in vars(self.workReport) for kwarg in kwargs):
            return False
        
        return self.workReportControl.changeOneEntry(entry, entryValue, **kwargs)


    def listWorkReports(self, **kwargs) -> list['WorkReport']:
        if any(kwarg not in vars(self.workReport) for kwarg in kwargs):
            return []

        workReports: list['WorkReport'] = self.workReportControl.readFile()
        if not len(kwargs):
            return workReports

        for k, v in kwargs.items():
            # Top to bottom if we go bottom to top we get index out of range
            # Because things get deleted if they do not match the query before we loop through them if we go bottom to top
            for i in range(len(workReports)-1, -1, -1):
                # hack around to check if result that might be int or float partialy contains our target number
                if str(v) not in str(workReports[i].__dict__[k]):
                    del workReports[i]

    # LIST WORK REPORTS MAYBE


        return workReports

    def currentWorkReportID(self, workOrderID: int) -> int:
        workReports: list['WorkReport'] = self.listWorkReports(workOrderID=workOrderID)
        if not len(workReports):
            return 1

        return workReports[-1].id+1


    def listByDateRange(self, start: str, end: str, **kwargs) -> list[WorkReport]:
        if not start:
            return self.listWorkReports(date=end, **kwargs)
        if not end:
            return self.listWorkReports(date=start, **kwargs)

        workReports: list[WorkReport] = self.listWorkReports(**kwargs)
        final: list[WorkReport] = []
        for workReport in workReports:
            if not workReport.date:
                continue
            if is_date_in_range(workReport.date, start, end):
                final.append(workReport)

        return final
