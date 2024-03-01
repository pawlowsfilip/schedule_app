from scheduler.scheduler import Scheduler
from datetime import datetime, time


class Scheduler_s(Scheduler):
    """
    Class representing a custom scheduler for duty at school.

    Args:
        accuracy (float): Desired accuracy of the scheduling process (accuracy of 1hr, 0.5hr, 0.25hr etc).
        allocation (dict): Dictionary representing worker allocations as {"start_time-end_time": number_of_workers}.
        variant (str): Variant identifier for the scheduling algorithm.
    """

    def __init__(self, time_frames, variant, start=None, stop=None):
        super().__init__(variant)

        self.time_frames = time_frames
        self.start = start
        self.stop = stop
        self.schedule = {}


