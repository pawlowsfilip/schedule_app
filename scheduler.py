from worker_manager import Worker_manager


class Scheduler():
    def __init__(self, variant):
        self.variant = variant
        self.worker_manager = Worker_manager()
