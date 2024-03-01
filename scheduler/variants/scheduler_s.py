from scheduler.scheduler import Scheduler
from datetime import datetime, time, timedelta


class Scheduler_s(Scheduler):
    """
    Class representing a custom scheduler for duty at school.

    """

    def __init__(self, time_frames: dict, variant: str, start=None, end=None) -> None:
        super().__init__(variant)

        self.time_frames = time_frames
        self.start = start
        self.end = end
        self.schedule = {}

    def _get_time_frames_list(self):
        time_frames = []

        for day, recesses in self.time_frames.items():
            for recess in recesses:
                time_frame = [recess["start"], recess["end"]]
                time_frames.append(time_frame)

        return time_frames

    def make_schedule(self):
        days = self.worker_manager.get_days()
        pass


    def _get_working_hours(self):
        pass