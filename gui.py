from scheduler import scheduler


class Gui:
    def __init__(self, everything):
        self.everything = everything
        self.scheduler = scheduler_factory().get_scheduler(variant_z_everything)

    def factory_method(self, ):
        pass

    def make_schedule(self):
        return self.scheduler.make_schedule()
