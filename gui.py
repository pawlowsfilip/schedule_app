from scheduler import scheduler
from scheduler_factory import SchedulerFactory
from scheduler.variants.scheduler_r import Scheduler_r


class Gui:
    def __init__(self, variant):
        self.scheduler = SchedulerFactory().get_scheduler(variant)

    def make_schedule(self):
        return self.scheduler.make_schedule()


test1 = Gui("R")
test_schedule = test1.make_schedule()
print(test_schedule)

"""
czasami są jakieś dziwne błedy ze na alokacji 1 dodaje mi druga osobe idk czemu
"""


def print_schedule(schedule):
    for day, time_frames in schedule.items():
        print(f"Schedule for {day}:")
        for time_frame, workers in time_frames.items():
            print(f"  Time Frame {time_frame}:")
            for worker in workers:
                # Assuming Worker objects have 'name' and 'position' attributes
                print(f"    Worker: {worker.name}, Position: {worker.position}")


print_schedule(test_schedule)
