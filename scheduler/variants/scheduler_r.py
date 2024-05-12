from scheduler.scheduler import Scheduler
from datetime import datetime, timedelta
from worker import Worker
import logging

logger = logging.getLogger(__name__)


class Scheduler_r(Scheduler):
    """
    Class representing a custom scheduler for restaurants.

    Args:
        accuracy (float): Desired accuracy of the scheduling process (accuracy of 1hr, 0.5hr, 0.25hr etc).
        allocation (dict): Dictionary representing worker allocations as {"start_time-end_time": number_of_workers}.
        variant (str): Variant identifier for the scheduling algorithm.
    """

    def __init__(self, variant: str, accuracy=None, allocation=None) -> None:
        logger.debug("Initializing the Scheduler_r")
        try:
            super().__init__(variant)
            self.accuracy = accuracy
            self.allocation = allocation
            self.schedule = {}
            logger.info(
                f"Scheduler_r initialized with variant: {variant}, accuracy: {accuracy}, allocation: {allocation}")
        except Exception as e:
            logger.error(f"Error initializing the Scheduler_r: {e}")
            raise

    def _get_working_hours(self):
        """
        Calculates the earliest start time and latest end time from the allocated time frames.

        Returns:
            tuple(str, str) or tuple(None, None): A tuple containing the earliest start time (HH:MM)
                                                and latest end time (HH:MM), or (None, None)
                                                if no time frames are allocated.
        """
        logger.debug("Getting working hours")
        earliest_start = None
        latest_end = None
        logger.debug(f"Current allocation: {self.allocation}")

        for day, time_ranges in self.allocation.items():
            for time_range in time_ranges.keys():
                try:
                    start_str, end_str = time_range.split("-")
                    start_time = self._parse_time(start_str.strip())
                    end_time = self._parse_time(end_str.strip())

                    if earliest_start is None or start_time < earliest_start:
                        earliest_start = start_time
                    if latest_end is None or end_time > latest_end:
                        latest_end = end_time
                except ValueError as e:
                    logger.error(f"Invalid time range: {time_range}. Exception: {e}")

        earliest_start_str = earliest_start.strftime('%H:%M') if earliest_start else None
        latest_end_str = latest_end.strftime('%H:%M') if latest_end else None
        logger.info(f"Earliest start: {earliest_start_str}, Latest end: {latest_end_str}")
        return earliest_start_str, latest_end_str

    def _number_of_time_frames_per_day(self):
        """
        Calculates the number of time frames per day based on the desired accuracy.

        Args:
            accuracy (float): Desired accuracy of the scheduling process (accuracy of 1hr, 0.5hr, 0.25hr etc).

        Returns:
            int: The number of time frames per day.
        """
        logger.debug("Calculating the number of time frames per day")
        start, end = self._get_working_hours()
        try:
            if start and end:
                start_time = datetime.strptime(start, '%H:%M')
                end_time = datetime.strptime(end, '%H:%M')

                total_time = (end_time - start_time).total_seconds() / 60
                time_frame_duration = int(self.accuracy * 60)

                num_frames = int(total_time / time_frame_duration)
                logger.debug(f"Calculated {num_frames} time frames per day based on accuracy {self.accuracy}")
                return num_frames
        except Exception as e:
            logger.error(f"Error calculating the number of time frames per day: {e}")
            return None

    def _get_time_frames_list(self):
        """
        Generates a list of time frames based on the desired accuracy.

        Returns:
            list: A list of time frames as strings.
        """
        logger.debug("Generating time frames list")
        start, end = self._get_working_hours()
        try:
            if start and end:
                start_time = datetime.strptime(start, '%H:%M')
                end_time = datetime.strptime(end, '%H:%M')
                accuracy_minutes = int(self.accuracy * 60)
                time_frames = []

                current_time = start_time

                while current_time < end_time:
                    next_time = current_time + timedelta(minutes=accuracy_minutes)
                    next_time = min(next_time, end_time)
                    time_frame_str = f"{current_time.strftime('%H:%M')}-{next_time.strftime('%H:%M')}"
                    time_frames.append(time_frame_str)
                    current_time = next_time

                logger.info(f"Generated sorted time frames list: {time_frames}")
                return time_frames
        except Exception as e:
            logger.error(f"Error generating time frames list: {e}")
            return None

    def get_needed_workers_for_time_frame(self, day, current_time_frame):
        """
        Calculates the number of workers needed for a given time frame on a given day.

        Args:
            day (str): The day for which the number of workers needed is calculated.
            current_time_frame (str): The current time frame for which the number of workers needed is calculated.

        Returns:
            int: The number of workers needed for the given time frame on the given day.
        """
        logger.debug(f"Calculating needed workers for time frame {current_time_frame} on day {day}")
        if not current_time_frame:
            return 0

        try:
            current_start_str, current_end_str = current_time_frame.split('-')
            current_start = self._parse_time(current_start_str)
            current_end = self._parse_time(current_end_str)

            if day in self.allocation:
                for time_frame, workers_needed in self.allocation[day].items():
                    start_str, end_str = time_frame.split('-')
                    start_time = self._parse_time(start_str)
                    end_time = self._parse_time(end_str)

                    if (start_time <= current_start < end_time) or (start_time < current_end <= end_time):
                        logger.info(f"Needed workers for day {day}, time frame {current_time_frame}: {workers_needed}")
                        return workers_needed
        except ValueError as e:
            logger.error(f"Invalid time frame: {current_time_frame}. Exception: {e}")

        logger.warning(f"No workers needed for day {day}, time frame {current_time_frame}")
        return 0

    def _get_least_used_workers(self):
        """
        Identifies and returns a list of workers with the minimum usage count within the schedule.
        If all workers have the same usage count, returns an empty list because they are equally used.

        Returns:
            list: A list of worker objects with the least usage count, or an empty list if no workers are available
            or all are equally used.
        """
        logger.debug("Identifying least used workers")
        worker_counts = {worker: 0 for worker in
                         self.worker_manager.workers_list}  # Initialize all workers with zero usage

        if worker_counts:
            for day_info in self.schedule.values():
                for workers in day_info.values():
                    for worker in workers:
                        if worker in worker_counts:
                            worker_counts[worker] += 1

            if len(set(worker_counts.values())) == 1:
                logger.info("All workers are used equally.")
                return []

            least_usage = min(worker_counts.values())
            least_used_workers = [worker for worker, count in worker_counts.items() if count == least_usage]

            logger.info(f"Least used workers: {least_used_workers[::-1]}")
            return least_used_workers[::-1]
        else:
            logger.warning("No workers available for scheduling.")
            return []

    def _get_previous_time_frame_worker(self, current_day, current_time_frame):
        """
        Finds the worker assigned to the previous time frame for the same day.

        Args:
            current_day (str): The day being checked.
            current_time_frame (str): The current time frame being checked.

        Returns:
            Worker: The worker assigned to the previous time frame, if available.
        """
        logger.debug(f"Finding previous time frame worker for day: {current_day}, current time frame: "
                     f"{current_time_frame}")
        sorted_time_frames = self._get_time_frames_list()  # This needs to return time frames in sorted order
        current_index = sorted_time_frames.index(current_time_frame)

        if current_index > 0:
            previous_time_frame = sorted_time_frames[current_index - 1]
            previous_workers = self.schedule.get(current_day, {}).get(previous_time_frame, [])

            for worker in previous_workers:
                if not isinstance(worker, Worker):
                    logger.warning(f"Invalid worker object: {worker}")
                    continue
                else:
                    if worker.is_available(current_day, current_time_frame):
                        logger.info(f"Previous time frame worker found: {worker.name} for day {current_day}, "
                                    f"time frame {current_time_frame}")
                        return worker

        logger.warning(f"No previous worker found for day {current_day}, time frame {current_time_frame}")
        return None

    def make_schedule(self):
        """
        Generates the schedule based on worker availability and position priorities.

        Returns:
            dict: The generated schedule.
        """
        logger.debug("Starting schedule generation.")
        days = self.worker_manager.get_days()
        time_frames = self._get_time_frames_list()

        logger.debug(f"Days identified for scheduling: {days}")
        logger.debug(f"Time frames available: {time_frames}")

        # Initialize an empty schedule
        self.schedule = {day: {time_frame: [] for time_frame in time_frames} for day in days}

        for day in days:
            logger.debug(f"Processing day: {day}")
            for time_frame in time_frames:
                needed_workers = self.get_needed_workers_for_time_frame(day, time_frame)
                logger.debug(f"Day: {day}, Time frame: {time_frame}, Needed workers: {needed_workers}")

                if needed_workers == 0:
                    logger.info(f"No workers required for day {day}, time frame {time_frame}. Skipping...")
                    continue

                workers_for_time_frame = []

                # 1. Sort workers based on the priorities
                sorted_workers = self.worker_manager.get_sorted_workers_by_position_priority()
                logger.debug(f"Sorted workers based on position priority: {[worker.name for worker in sorted_workers]}")

                # Reverse the order, because the higher value, the lower position worker has.
                for worker in sorted_workers[::-1]:
                    # Skip if the time frame already has the needed workers
                    if len(workers_for_time_frame) >= needed_workers:
                        logger.info(f"Required workers assigned for day {day}, time frame {time_frame}.")
                        break

                    # 2. Check if previous worker on that position is still available
                    if worker == self._get_previous_time_frame_worker(day, time_frame) and worker.is_available(
                            day, time_frame):
                        if worker not in workers_for_time_frame:
                            workers_for_time_frame.append(worker)
                            logger.info(f"Assigned previous time frame worker: {worker.name} for day {day}, "
                                        f"time frame {time_frame}.")
                            continue

                    # Skip if the time frame already has the needed workers
                    if len(self.schedule[day][time_frame]) >= needed_workers:
                        break

                    # 3. Check the least used worker on that position is still available
                    least_used_workers = self._get_least_used_workers()
                    for least_used_worker in least_used_workers:
                        if least_used_worker.position == worker.position and least_used_worker.is_available(
                                day, time_frame):
                            if least_used_worker not in workers_for_time_frame:
                                workers_for_time_frame.append(least_used_worker)
                                logger.info(f"Assigned least-used worker: {least_used_worker.name} for day {day},"
                                            f" time frame {time_frame}.")
                                break
                    # Skip if the time frame already has the needed workers
                    if len(self.schedule[day][time_frame]) >= needed_workers:
                        break

                    # 4. Check the available workers on that position
                    if worker.is_available(day, time_frame) and worker not in workers_for_time_frame:
                        workers_for_time_frame.append(worker)
                        logger.info(f"Assigned available worker: {worker.name} for day {day}, time frame {time_frame}.")
                        continue

                    # Skip if the time frame already has the needed workers
                    if len(workers_for_time_frame) >= needed_workers:
                        break

                    # 5. Check the available if needed on that position.
                    if worker.is_available_if_needed(day, time_frame) and worker not in workers_for_time_frame:
                        workers_for_time_frame.append(worker)
                        logger.info(f"Assigned 'if needed' worker: {worker.name} for day {day}, "
                                    f"time frame {time_frame}.")
                        continue

                    # Skip if the time frame already has the needed workers
                    if len(self.schedule[day][time_frame]) >= needed_workers:
                        break

                while len(workers_for_time_frame) < needed_workers:
                    workers_for_time_frame.append("NO WORKER")
                    logger.warning(f"No worker available for day {day}, time frame {time_frame}. "
                                   f"Marked as 'NO WORKER'.")

                if all(worker == "NO WORKER" for worker in workers_for_time_frame):
                    workers_for_time_frame = ["NO WORKER AVAILABLE"]
                    logger.warning(f"Day {day}, time frame {time_frame} has no available workers.")

                self.schedule[day][time_frame] = workers_for_time_frame

        logger.info(f"Schedule generation complete: {self.schedule}")
        return self.schedule
