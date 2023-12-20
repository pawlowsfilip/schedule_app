from worker_manager import Worker_Manager


class Scheduler:
    def __init__(self, variant):
        self.variant = variant
        self.worker_manager = Worker_Manager()

    # klasa ktora bedzie dziedziczona przez scheduler_r i _s
