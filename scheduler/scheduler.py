from worker_manager import Worker_Manager
from worker import Worker
from datetime import datetime, timedelta
from abc import ABC, abstractmethod


class Scheduler(ABC):
    def __init__(self, variant):
        # worker1 = Worker('Filip', {'21.07': '8:00-10:00'}, {'21.07': '7:00-10:00'}, 'Manager')
        # worker2 = Worker('Natalia', {'21.07': '8:00-10:00'}, {}, 'Regular')
        # worker3 = Worker('Ola', {'21.07': '8:00-9:00'}, {'21.07': '10:00-14:00'}, 'Student')
        # worker4 = Worker('Kondziu', {'21.07': '10:00-14:00'}, {'21.07': '10:00-14:00'}, 'Student')
        # wm1 = Worker_Manager(worker1, worker2, worker3, worker4)
        # wm1.set_position_priorities({'Manager': 1, 'Regular': 2, "Student": 3})
        # self.worker_manager = wm1

        self.variant = variant
        self.schedule = {}
        self.worker_manager = Worker_Manager()

    @abstractmethod
    def _get_previous_time_frame_worker(self, current_day, current_time_frame):
        pass

    @abstractmethod
    def _get_least_used_workers(self):
        pass

    @abstractmethod
    def _get_time_frames_list(self):
        pass

    @abstractmethod
    def make_schedule(self):
        pass

    @abstractmethod
    def _get_working_hours(self):
        pass

    @abstractmethod
    def get_needed_workers_for_time_frame(self, current_time_frame):
        pass

    @staticmethod
    def _parse_time(time_str):
        return datetime.strptime(time_str, "%H:%M").time()
