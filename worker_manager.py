from worker import Worker
import logging

logger = logging.getLogger(__name__)


class Worker_Manager:
    def __init__(self, *workers):
        logger.debug("Initializing Worker_Manager")
        try:
            self.workers_list = self.make_workers(*workers)
            self.position_priorities = {}
            logger.info("Worker_Manager initialized with %d workers", len(self.workers_list))
        except Exception as e:
            logger.error(f"Error initializing Worker_Manager: {e}")
            raise

    @staticmethod
    def make_workers(*workers):
        workers_list = []
        if workers:
            workers_list.extend(workers)
            logger.info("Created workers list with %d workers", len(workers_list))
        return workers_list

    def set_position_priorities(self, priorities):
        """
        Dynamically sets or updates the priorities of positions.
        The priorities parameter should be a dictionary mapping position names to their priorities.
        Lower numbers indicate higher priority (first to assign to time_frame).

        :param priorities: Dict[str, int]
        """
        if priorities is None:
            logger.warning("No position priorities provided.")
        elif not isinstance(priorities, dict):
            logger.error("Invalid priorities format. Expected a dictionary.")
            return None

        if self.position_priorities:
            logger.info("Updating existing position priorities")
            self.position_priorities = priorities
            return self.position_priorities
        else:
            logger.info("Could not update position priorities, returning workers list")
            return self.workers_list

    def _get_position_priority(self, position):
        """
        Retrieves the priority of a given position.
        If the position is not found, a default high priority number is returned,
        ensuring it is treated as lower priority compared to defined ones.

        :param position: str
        :return: int
        """
        priority = self.position_priorities.get(position, 9999)
        logger.debug("Retrieved priority for position '%s': %d", position, priority)
        return priority

    def get_sorted_workers_by_position_priority(self):
        """
        Returns workers sorted by their position priority.
        Workers without a defined position are treated as the lowest priority.
        Higher numbers to lower-priority positions.
        """
        if self.position_priorities:
            sorted_workers = sorted(self.workers_list, key=lambda worker: self._get_position_priority(worker.position))
            logger.debug(f"Sorted workers by position priority: {sorted_workers}")
            return sorted_workers
        else:
            logger.info("No position priorities defined, returning workers list as-is")
            return self.workers_list

    def get_available_workers(self, day, time_frame):
        available_workers = []
        for worker in self.workers_list:
            if worker.is_available(day, time_frame):
                available_workers.append(worker)
        logger.info("Found %d available workers for day '%s' and time frame '%s'",
                    len(available_workers), day, time_frame)

        return available_workers

    def get_available_workers_if_needed(self, day, time_frame):
        available_workers_if_needed = []
        for worker in self.workers_list:
            if worker.is_available_if_needed(day, time_frame):
                available_workers_if_needed.append(worker)
        logger.info("Found %d workers available if needed for day '%s' and time frame '%s'",
                    len(available_workers_if_needed), day, time_frame)
        return available_workers_if_needed

    def remove_worker(self, worker):
        if worker in self.workers_list:
            self.workers_list.remove(worker)
            logger.info("Removed worker: %s", worker.name)
            return True
        else:
            logger.warning("Worker '%s' not found in the list", worker.name)
            return False

    def get_days(self):
        if not self.workers_list:
            logger.warning("No workers are available to retrieve days from")
            return []

        # changed, can be a problem
        days = next(iter(self.workers_list)).availability.keys()
        logger.debug("Retrieved available days: %s", list(days))
        return days

    def get_hours(self, day):
        logger.debug("Retrieving hours for day '%s'", day)
        for worker in self.workers_list:
            for key in worker.availability.keys():
                if key == day:
                    hours = worker.availability[day]
                    logger.debug("Retrieved hours for day '%s': %s", day, hours)
                    return hours
