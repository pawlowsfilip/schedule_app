from worker_manager import Worker_Manager
from worker import Worker


class Scheduler:
    def __init__(self, variant):
        # worker1 = Worker('Filip', {}, {}, 'Manager')
        worker2 = Worker('Natalia', {'21.07': '10:00-14:00'}, {}, 'Student')
        worker3 = Worker('Ola', {'21.07': '8:00-9:00'}, {}, 'Student')
        worker4 = Worker('Kondziu', {'21.07': '7:00-10:00'}, {'21.07': '10:00-14:00'}, 'Student')
        wm1 = Worker_Manager(worker2, worker3, worker4)

        self.variant = variant
        # self.worker_manager = Worker_Manager()
        self.worker_manager = wm1

    # klasa ktora bedzie dziedziczona przez scheduler_r i _s
