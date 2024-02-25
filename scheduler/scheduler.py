from worker_manager import Worker_Manager
from worker import Worker


class Scheduler:
    def __init__(self, variant):
        worker1 = Worker('Filip', {'21.07': '8:00-10:00'}, {}, 'Manager')
        worker2 = Worker('Natalia', {'21.07': '8:00-10:00'}, {}, 'Regular')
        worker3 = Worker('Ola', {'21.07': '8:00-9:00'}, {'21.07': '10:00-14:00'}, 'Student')
        worker4 = Worker('Kondziu', {'21.07': '10:00-14:00'}, {'21.07': '10:00-14:00'}, 'Student')
        wm1 = Worker_Manager(worker1, worker2, worker3, worker4)
        wm1.set_position_priorities({'Manager': 1, 'Regular': 2, "Student": 3})

        self.variant = variant
        # self.worker_manager = Worker_Manager()
        self.worker_manager = wm1

    # klasa ktora bedzie dziedziczona przez scheduler_r i _s
