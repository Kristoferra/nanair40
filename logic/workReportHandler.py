from baseClasses.workReport import WorkReport
from dataControl.workReportController import WorkReportController
from typing import Any


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

