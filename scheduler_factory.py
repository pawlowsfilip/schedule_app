from scheduler.variants.scheduler_r import Scheduler_r
from scheduler.variants.scheduler_s import Scheduler_s


class SchedulerFactory:
    @staticmethod
    def get_scheduler(variant, **kwargs):
        if variant == 'R':
            return Scheduler_r(variant, **kwargs)
        if variant == 'S':
            return Scheduler_s(variant, **kwargs)
        else:
            return None
