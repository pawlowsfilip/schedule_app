from scheduler.scheduler import Scheduler
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def extract_start_time(time_frame):
    start_str, _ = time_frame.split('-')
    return datetime.strptime(start_str.strip(), '%H:%M')

class Scheduler_s(Scheduler):
    """
    Class representing a custom scheduler for duty at school.

    """

    def __init__(self, variant: str, allocation=None) -> None:
        logger.debug("Initializing Scheduler_s")
        try:
            super().__init__(variant)
            self.allocation = allocation
            self.schedule = {}
            logger.debug(f"Scheduler_s initialized with variant {variant} and allocation {allocation}")
        except Exception as e:
            logger.error(f"Error initializing Scheduler_s: {e}")
            raise

    def _get_time_frames_list(self):
        logger.debug("Generating list of time frames.")
        try:
            time_frames = set()
            for day_time_frames in self.allocation.values():
                for time_frame in day_time_frames:
                    time_frames.add(time_frame)

            sorted_time_frames = sorted(list(time_frames), key=extract_start_time)
            logger.debug(f"Sorted time frames: {sorted_time_frames}")
            return sorted_time_frames

        except Exception as e:
            logger.error(f"Error generating list of time frames: {e}")
            raise

    def get_needed_workers_for_time_frame(self, day, current_time_frame):
        try:
            if day in self.allocation and current_time_frame in self.allocation[day]:
                needed_workers = self.allocation[day][current_time_frame]
                logger.debug(f"Needed workers for {day}, {current_time_frame}: {needed_workers}")
                return needed_workers
            logger.warning(f"No allocation found for {day}, {current_time_frame}")
            return None
        except Exception as e:
            logger.error(f"Error getting needed workers for {day}, {current_time_frame}: {e}")
            raise

    def _get_previous_time_frame_worker(self, current_day, current_time_frame):
        try:
            logger.debug(f"Getting previous time frame worker for {current_day}, {current_time_frame}")
            sorted_time_frames = self._get_time_frames_list()  # This needs to return time frames in sorted order
            current_index = sorted_time_frames.index(current_time_frame)

            if current_time_frame not in sorted_time_frames:
                logger.error(f"Time frame {current_time_frame} not found in schedule.")
                raise ValueError(f"Time frame {current_time_frame} not found in schedule.")

            if current_index > 0:
                previous_time_frame = sorted_time_frames[current_index - 1]
                day_schedule = self.schedule.get(current_day, {})

                if previous_time_frame in day_schedule:
                    previous_workers = day_schedule[previous_time_frame]
                    for worker in previous_workers:
                        if worker == 'NO WORKER' or worker == 'NO WORKER AVAILABLE':
                            continue
                        else:
                            if worker.is_available(current_day, current_time_frame):
                                logger.debug(f"Previous time frame worker found: {worker.name}")
                                return worker
            logger.debug("No previous time frame worker found.")
            return None
        except Exception as e:
            logger.error(f"Error getting previous time frame worker for {current_day}, {current_time_frame}: {e}")
            raise

    def _get_least_used_workers(self):
        """
        Identifies and returns a worker with the minimum usage count within the schedule.

        Returns:
            str or None: The name of a randomly selected worker with the least usage count,
                        or None if no workers are available.
        """
        try:
            logger.debug("Identifying least used workers.")
            worker_counts = {worker: 0 for worker in
                             self.worker_manager.workers_list}  # Initialize all workers with zero usage

            if worker_counts:
                for day_schedule in self.schedule.values():
                    for time_frame, workers in day_schedule.items():
                        for worker in workers:
                            if worker in worker_counts:
                                worker_counts[worker] += 1

                # Check if all workers are used equally
                if len(set(worker_counts.values())) == 1:
                    logger.debug("All workers are used equally.")
                    return []

                # Get the worker with the minimum usage count
                least_usage = min(worker_counts.values())
                least_used_workers = [worker for worker, count in worker_counts.items() if count == least_usage]

                logger.debug(f"Least used workers: {least_used_workers}")
                return least_used_workers[::-1]
            else:
                logger.warning("No workers available for counting.")
                return []
        except Exception as e:
            logger.error(f"Error identifying least used workers: {e}")
            raise

    def make_schedule(self):
        try:
            logger.debug("Starting schedule generation.")
            days = self.worker_manager.get_days()
            self.schedule = {day: {} for day in days}

            for day in days:
                logger.debug(f"Processing day: {day}")
                time_frames = self.allocation[day].keys()
                day_schedule = {}  # This will hold all time frame dictionaries for the current day

                for time_frame in time_frames:
                    needed_workers = self.get_needed_workers_for_time_frame(day, time_frame)
                    logger.debug(f"Day: {day}, Time frame: {time_frame}, Needed workers: {needed_workers}")
                    workers_for_time_frame = []  # This will collect workers for the current time frame

                    if needed_workers == 0:
                        logger.info(f"No workers required for day {day}, time frame {time_frame}. Skipping...")
                        continue

                    if len(workers_for_time_frame) < needed_workers:
                        # 1. Try to get previous worker
                        previous_worker = self._get_previous_time_frame_worker(day, time_frame)
                        if previous_worker and previous_worker.is_available(day, time_frame) and \
                                previous_worker not in workers_for_time_frame:
                            workers_for_time_frame.append(previous_worker)
                            logger.info(f"Assigned previous time frame worker: {previous_worker.name} for day {day}, time frame {time_frame}.")

                        # 2. Try to get least used worker
                        least_used_workers = self._get_least_used_workers()
                        for worker in least_used_workers:
                            if len(workers_for_time_frame) < needed_workers and worker not in workers_for_time_frame \
                                    and worker.is_available(day, time_frame):
                                workers_for_time_frame.append(worker)
                                logger.info(f"Assigned least-used worker: {worker.name} for day {day}, time frame {time_frame}.")

                        # 3. Try to get worker by normal availability
                        available_workers = self.worker_manager.get_available_workers(day, time_frame)
                        for worker in available_workers:
                            if len(workers_for_time_frame) < needed_workers and worker not in workers_for_time_frame:
                                workers_for_time_frame.append(worker)
                                logger.info(f"Assigned available worker: {worker.name} for day {day}, time frame {time_frame}.")

                        # 4. Try to worker by worse availability
                        if len(workers_for_time_frame) < needed_workers:
                            available_if_needed_workers = self.worker_manager.get_available_workers_if_needed(day,
                                                                                                              time_frame)
                            for worker in available_if_needed_workers:
                                if len(workers_for_time_frame) < needed_workers and worker not in workers_for_time_frame:
                                    workers_for_time_frame.append(worker)
                                    logger.info(f"Assigned 'if needed' worker: {worker.name} for day {day}, time frame {time_frame}.")

                        while len(workers_for_time_frame) < needed_workers:
                            workers_for_time_frame.append("NO WORKER")
                            logger.warning(f"No worker available for day {day}, time frame {time_frame}. Marked as 'NO WORKER'.")

                    if all(worker == "NO WORKER" for worker in workers_for_time_frame):
                        workers_for_time_frame = ["NO WORKER AVAILABLE"]
                        logger.warning(f"Day {day}, time frame {time_frame} has no available workers.")

                    day_schedule[time_frame] = workers_for_time_frame
                    self.schedule[day] = day_schedule

            logger.info(f"Schedule generation complete: {self.schedule}")
            return self.schedule
        except Exception as e:
            logger.error(f"Error generating schedule: {e}")
            raise

    def _get_working_hours(self):
        pass
