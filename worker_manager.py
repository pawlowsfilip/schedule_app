from worker import Worker


class Worker_Manager:
    def __init__(self, *workers):
        self.workers_list = self.make_workers(*workers)

    def __str__(self):
        worker_info = ""
        for worker in self.workers_list:
            worker_info += f"Name: {worker.name}, Position: {worker.position}, Availability: {worker._availability}, Worse availability: {worker._worse_availability}\n"
        return worker_info

    @staticmethod
    def make_workers(*workers):
        workers_list = []

        if workers:
            workers_list.extend(workers)

        else:
            while True:
                name = input("Enter workers name (or type 'exit' to finish): ")
                if name.lower() == 'exit':
                    break

                position = input("Enter worker's position: ")
                availability = input("Enter worker's availability: ")
                worse_availability = input("Enter worker's worse availability: ")

                worker = Worker(name, availability, worse_availability, position)

                workers_list.append(worker)

        return workers_list

    def get_available_workers(self, day, time_frame):
        available_workers = []
        for worker in self.workers_list:
            if worker.is_available(day, time_frame):
                available_workers.append(worker)
        return available_workers

    def get_available_workers_if_needed(self, day, time_frame):
        available_workers_if_needed = []
        for worker in self.workers_list:
            if worker.is_available_if_needed(day, time_frame):
                available_workers_if_needed.append(worker)
        return available_workers_if_needed

    def remove_worker(self, worker):
        if worker in self.workers_list:
            self.workers_list.remove(worker)
            return True

    def get_days(self):
        for worker in self.workers_list:
            return worker.availability.keys()

    def get_hours(self, day):
        for worker in self.workers_list:
            for key in worker.availability.keys():
                if key == day:
                    return worker.availability[day]
