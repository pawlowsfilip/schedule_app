from scheduler.variants.scheduler_r import Scheduler_r
from scheduler.variants.scheduler_s import Scheduler_s


class SchedulerFactory:
    @staticmethod
    def get_scheduler(variant, **kwargs):
        if variant == 'R':
            """
            For testing
            """
            # accuracy = 1.0
            # allocation = {"7:00-10:00": 1, "10:00-14:00": 2}
            return Scheduler_r(variant, **kwargs)
        if variant == 'S':
            return Scheduler_s(variant, **kwargs)
        else:
            return None
