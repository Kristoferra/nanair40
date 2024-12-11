from logic.logicWrapper import Logic_Wrapper
from baseClasses.workReport import WorkReport


x = Logic_Wrapper()
wr = WorkReport(32, 1, "test", 1, 1, "12.12.2024", 500, "test", True)
print(x.addWorkReport(wr))
