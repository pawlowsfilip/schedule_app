from scheduler_r import scheduler_r
from scheduler_s import scheduler_s

class SchedulerFactory:
    @staticmethod
    def get_scheduler(variant):
        if variant == 'R':
            return scheduler_r()
        if variant == 'S':
            return scheduler_s()
