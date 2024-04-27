from scheduler import scheduler
from scheduler_factory import SchedulerFactory
from scheduler.variants.scheduler_r import Scheduler_r
from excel_exporter import ExcelExporter


class Gui:
    def __init__(self, variant):
        self.scheduler = SchedulerFactory().get_scheduler(variant)

    def make_schedule(self):
        return self.scheduler.make_schedule()

    def export_schedule(self):
        schedule = self.make_schedule()
        return ExcelExporter(schedule).export_to_excel()

#
# test1 = Gui("R")
# test_schedule = test1.make_schedule()
#
# test1.export_schedule()
#
# print(test_schedule)
