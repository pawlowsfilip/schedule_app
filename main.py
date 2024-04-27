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
