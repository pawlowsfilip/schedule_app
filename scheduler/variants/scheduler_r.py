from scheduler.scheduler import Scheduler
from worker_manager import Worker_Manager
import datetime


class Scheduler_r(Scheduler):
    def __init__(self, accuracy, allocation, variant):
        super().__init__(variant)
        self.accuracy = accuracy
        self.allocation = allocation        # {1:"7:00-10:00", ...} z tego mozna wyciagnac kiedyy poczatek i koniec pracy
        self.worker_manager = Worker_Manager()

    def _get_previous_time_frame_worker(self, time_frame):
        pass

    def _get_least_used_workers(self):
        pass

    def _get_working_hours(self):
        start = list(self.allocation.values())[0]
        end = list(self.allocation.values())[-1]

        start = start.split('-')[0]
        end = end.split('-')[-1]

        return start, end

    def do_this_shit(self):
        positions = set([worker.position for worker in self.worker_manager.workers_list])
        days = self.worker_manager.get_days()
        start, end = self._get_working_hours()

        if not positions:
            positions = ['placeholder']

        for position in positions:
            for day in days:
                for time_frame in range(time_frames):
                    while len(positions)

