from scheduler import scheduler
from scheduler_factory import SchedulerFactory
from scheduler.variants.scheduler_r import Scheduler_r


class Gui:
    def __init__(self, variant):
        self.scheduler = SchedulerFactory().get_scheduler(variant)

    def make_schedule(self):
        return self.scheduler.make_schedule()

    def export_schedule(self):
        self.scheduler.export_to_excel()


test1 = Gui("R")
test_schedule = test1.make_schedule()

test1.export_schedule()

print(test_schedule)


def print_schedule(schedule):
    for day, time_frames in schedule.items():
        print(f"Schedule for {day}:")
        for time_frame, workers in time_frames.items():
            print(f"  Time Frame {time_frame}:")
            if workers:  # Check if the list of workers is not empty
                for worker in workers:
                    # Check if worker is a string indicating no workers available or an actual Worker object
                    if isinstance(worker, str) and worker == "No worker available":
                        print(f"    {worker}")  # Print the string directly
                    elif worker:  # This checks if worker is not None and not the "No worker available" string
                        print(f"    Worker: {worker.name}, Position: {worker.position}")
            else:
                print("No workers available")  # This line handles the case if workers list is empty


print_schedule(test_schedule)
