from scheduler.scheduler import Scheduler
from datetime import datetime, time


class Scheduler_s(Scheduler):
    """
    Class representing a custom scheduler for duty at school.

    """

    def __init__(self, time_frames: dict, variant: str, start=None, stop=None) -> None:
        super().__init__(variant)

        self.time_frames = time_frames
        self.start = start
        self.stop = stop
        self.schedule = {}


