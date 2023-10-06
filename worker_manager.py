from worker import Worker


class Worker_Manager:
    def __init__(self):
        self.workers_list = []

    def add_worker(self, name, availability, position=None, worse_availability=None):
        worker = Worker(name=name, availability=availability, position=position, worse_availability=worse_availability)
        self.workers_list.append(worker)

    def remove_worker(self, worker):
        self.workers_list.remove(worker)

    def get_days(self):
        for worker in self.workers_list:
            return worker.availability.keys()

    def get_hours(self, day):
        for worker in self.workers_list:
            for key in worker.availability.keys():
                if key == day:
                    return worker.availability[day]

    def get_available_workers_via_availability(self, day, time_frame, position):
        for worker in self.workers_list:
            for key in worker.availability.keys():
                if key == day:
                    if worker.availability[day] in time_frame:
                        return worker.name, worker.availability[day]
                    # trzeba zmienić tutaj time frame na jakiś typ danych dlatego zeby wyszukac czy miescie sie
                    # przedziale

    def get_available_workers_via_worse_availability(self, day, time_frame, position):
        # trzeba zmienić tutaj time frame na jakiś typ danych dlatego zeby wyszukac czy miescie sie
        # przedziale
        pass

    def is_worker_available(self):
        pass

    def get_workers_available_on_day(self, day):
        pass

    def get_workers_worse_available_on_day(self, day):
        pass

