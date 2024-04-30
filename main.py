from scheduler_factory import SchedulerFactory
from excel_exporter import ExcelExporter


class Gui:
    def __init__(self, variant):
        self.scheduler = SchedulerFactory().get_scheduler(variant)

    def make_schedule(self):
        return self.scheduler.make_schedule()

    def export_schedule(self):
        schedule = self.make_schedule()
        return ExcelExporter(schedule).export_to_excel()

    def update_accuracy(self, accuracy):
        self.scheduler.accuracy = accuracy
        print("Accuracy updated to:", accuracy)

    def update_allocation(self, allocation):
        self.scheduler.allocation = allocation
        print("Allocation updated to:", allocation)

    def update_time_frames(self, time_frames):
        self.scheduler.time_frames = time_frames
        print("Time frames updated to:", time_frames)

    def update_name(self, name):
        self.scheduler.name = name
        print("Name updated to:", name)

    def update_availability(self, availability):
        self.scheduler.availability = availability
        print("Availability updated to:", availability)

    def update_worse_availability(self, worse_availability):
        self.scheduler.worse_availability = worse_availability
        print("Worse availability updated to:", worse_availability)

    def update_position(self, position):
        self.scheduler.position = position
        print("Position updated to:", position)
