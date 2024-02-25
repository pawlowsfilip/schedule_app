from worker import Worker


class Worker_Manager:
    def __init__(self, *workers):
        self.workers_list = self.make_workers(*workers)
        self.position_priorities = {}

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
                    return workers_list

                position = input("Enter worker's position: ")
                availability = input("Enter worker's availability: ")
                worse_availability = input("Enter worker's worse availability: ")

                worker = Worker(name, availability, worse_availability, position)

                workers_list.append(worker)
        return workers_list

    def set_position_priorities(self, priorities):
        """
        Dynamically sets or updates the priorities of positions.
        The priorities parameter should be a dictionary mapping position names to their priorities.
        Lower numbers indicate higher priority.

        :param priorities: Dict[str, int]
        """
        self.position_priorities = priorities

    def _get_position_priority(self, position):
        """
        Retrieves the priority of a given position.
        If the position is not found, a default high priority number is returned,
        ensuring it is treated as lower priority compared to defined ones.

        :param position: str
        :return: int
        """
        return self.position_priorities.get(position, 9999)

    def get_sorted_workers_by_position_priority(self):
        """
        Returns workers sorted by their position priority.
        Workers without a defined position are treated as the lowest priority.
        """
        # Sort workers based on the position priority, then by name or another attribute for consistency.
        return sorted(self.workers_list, key=lambda worker: self._get_position_priority(worker.position), reverse=True)

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
