from scheduler_factory import SchedulerFactory
from excel_exporter import ExcelExporter
import json

from worker import Worker
from worker_manager import Worker_Manager


class Gui:
    def __init__(self, variant):
        self.scheduler = SchedulerFactory().get_scheduler(variant)

    def make_schedule(self):
        return self.scheduler.make_schedule()

    def export_schedule(self):
        print('making schedule')
        schedule = self.make_schedule()
        print('Schedule data:', schedule)
        return ExcelExporter(schedule).export_to_excel()

    def update_day(self, day):
        self.scheduler.day = accuracy
        print("Accuracy updated to:", day)

    def update_accuracy(self, accuracy):
        self.scheduler.accuracy = accuracy
        print("Accuracy updated to:", accuracy)

    def update_allocation(self, allocation):
        self.scheduler.allocation = allocation
        print("Allocation updated to:", allocation)

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

    def update_workers(self, workers):
        self.scheduler.worker_manager = Worker_Manager(*workers)
        print("Workers updated")

    @staticmethod
    def read_json_data(filepath):
        with open(filepath, 'r') as file:
            return json.load(file)

    def update_scheduler_from_json(self, filepath):
        data = self.read_json_data(filepath)
        allocation = {}
        workers = []

        for entry in data:
            if "time_frames" in entry:
                time_frames_str = entry["time_frames"]
                time_frame_list = [tf.strip() for tf in time_frames_str.split(",")]

                for tf in time_frame_list:
                    time_frame, workers_needed = map(str.strip, tf.rsplit(":", 1))
                    allocation[time_frame] = int(workers_needed)


            elif "name" in entry:
                workers.append(Worker(
                    name=entry["name"],
                    availability=entry["availability"],
                    worse_availability=entry["worse_availability"]
                ))

        self.update_allocation(allocation)
        self.update_workers(workers)

    def print_scheduler_data(self):
        print("Allocation:", self.scheduler.allocation)
        print("Name:", getattr(self.scheduler, "name", "Not Available"))
        print("Availability:", getattr(self.scheduler, "availability", "Not Available"))
        print("Worse Availability:", getattr(self.scheduler, "worse_availability", "Not Available"))

