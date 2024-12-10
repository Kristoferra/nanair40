from logic.logicWrapper import Logic_Wrapper
from baseClasses.workReport import WorkReport

lw = Logic_Wrapper()


workReport = WorkReport(1, 1, "test", 1, "25", 100, "haha")

print(lw.addWorkReport(workReport))



