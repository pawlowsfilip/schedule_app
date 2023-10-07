from worker import Worker
from time_utils import *


class Worker_Manager:
    def __init__(self):
        self.workers_list = []

    def add_worker(self, name, worker_availability, worse_availability=None, position=None):
        worker = Worker(name=name, availability=worker_availability,
                        worse_availability=worse_availability, position=position)
        self.workers_list.append(worker)

    def remove_worker(self, worker):
        self.workers_list.remove(worker)

    def get_days(self):
        for worker in self.workers_list:
            return worker.availability.keys()

    def get_hours(self, day):
        for worker in self.workers_list:
            for key in worker.availability.keys():
                if key == day:
                    return worker.availability[day]

    def get_position(self, worker):
        for worker in self.workers_list:
            return worker.position

    @staticmethod
    def check_availability(worker, day, required_start, required_end):
        return is_available(worker.availability[day], required_start, required_end)

    @staticmethod
    def check_worse_availability(worker, day, required_start, required_end):
        return is_available(worker.worse_availability[day], required_start, required_end)

    def get_available_workers_via_availability(self, day, time_frame, position=None):
        workers_list = []
        required_start, required_end = time_frame_split(time_frame)
        for worker in self.workers_list:
            if position is None or self.get_position(worker) == position:
                if day in self.get_days():
                    if self.check_availability(worker, day, required_start, required_end):
                        workers_list.append(worker)
        return workers_list

    def get_available_workers_via_worse_availability(self, day, time_frame, position=None):
        workers_list = []
        required_start, required_end = time_frame_split(time_frame)
        for worker in self.workers_list:
            if position is None or self.get_position(worker) == position:
                if day in self.get_days():
                    if self.check_worse_availability(worker, day, required_start, required_end):
                        workers_list.append(worker)
        return workers_list

    def is_worker_available(self):
        pass

    def get_workers_available_on_day(self, day):
        pass

    def get_workers_worse_available_on_day(self, day):
        pass
