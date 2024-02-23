from scheduler.variants.scheduler_r import Scheduler_r
#from scheduler.variants.scheduler_s import Scheduler_s


class SchedulerFactory:
    @staticmethod
    def get_scheduler(variant):
        if variant == 'R':
            # Default, testing arguments:
            accuracy = 1.0
            allocation = {"7:00-10:00": 1, "10:00-14:00": 2}
            return Scheduler_r(accuracy, allocation, variant)
        # if variant == 'S':
        #     return Scheduler_s()
