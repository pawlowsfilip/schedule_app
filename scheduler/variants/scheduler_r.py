import random

from scheduler.scheduler import Scheduler
from worker_manager import Worker_Manager
from datetime import datetime, timedelta


class Scheduler_r(Scheduler):
    """
    Class representing a custom scheduler for restaurants.

    Args:
        accuracy (float): Desired accuracy of the scheduling process (accuracy of 1hr, 0.5hr, 0.25hr etc).
        allocation (dict): Dictionary representing worker allocations as {"start_time-end_time": number_of_workers}.
        variant (str): Variant identifier for the scheduling algorithm.
    """

    def __init__(self, accuracy, allocation, variant):
        super().__init__(variant)

        self.accuracy = accuracy
        self.allocation = allocation  # {"7:00-10:00": 1, ...} z tego mozna wyciagnac kiedyy poczatek i koniec pracy i ilosc pracownnikow
        self.schedule = {}

    def _get_working_hours(self):
        """
        Calculates the earliest start time and latest end time from the allocated time frames.

        Returns:
            tuple(str, str) or tuple(None, None): A tuple containing the earliest start time (HH:MM)
                                                and latest end time (HH:MM), or (None, None)
                                                if no time frames are allocated.
        """
        earliest_start = None
        latest_end = None

        for time_range in self.allocation.keys():
            start_str, end_str = time_range.split("-")
            start_time = self._parse_time(start_str)
            end_time = self._parse_time(end_str)

            if earliest_start is None or start_time < earliest_start:
                earliest_start = start_time
            if latest_end is None or end_time > latest_end:
                latest_end = end_time

        earliest_start_str = earliest_start.strftime('%H:%M') if earliest_start else None
        latest_end_str = latest_end.strftime('%H:%M') if latest_end else None

        return earliest_start_str, latest_end_str

    # def _get_working_hours(self):
    #     """
    #     Calculates the earliest start time and latest end time from the allocated time frames.
    #
    #     Returns:
    #         tuple(str, str) or tuple(None, None): A tuple containing the earliest start time (HH:MM)
    #                                             and latest end time (HH:MM), or (None, None)
    #                                             if no time frames are allocated.
    #     """
    #     earliest_start = None
    #     latest_end = None
    #
    #     for time_frames in self.allocation.values():
    #         for time_frame in time_frames.split(","):
    #             start_str, end_str = time_frame.split("-")
    #             start_time = self._parse_time(start_str)
    #             end_time = self._parse_time(end_str)
    #
    #             if earliest_start is None or start_time < earliest_start:
    #                 earliest_start = start_time
    #             if latest_end is None or end_time > latest_end:
    #                 latest_end = end_time
    #
    #     earliest_start_str = earliest_start.strftime('%H:%M') if earliest_start else None
    #     latest_end_str = latest_end.strftime('%H:%M') if latest_end else None
    #
    #     return earliest_start_str, latest_end_str

    def _number_of_time_frames_per_day(self, accuracy):
        """
        Calculates the number of time frames per day based on the desired accuracy.

        Args:
            accuracy (float): Desired accuracy of the scheduling process (accuracy of 1hr, 0.5hr, 0.25hr etc).

        Returns:
            int: The number of time frames per day.
        """
        start, end = self._get_working_hours()
        # having the strptime because it is easier to subtract end from start
        start_time = datetime.strptime(start, '%H:%M')
        end_time = datetime.strptime(end, '%H:%M')

        # calculate the time frame in minutes
        total_time = (end_time - start_time).total_seconds() / 60
        time_frame_duration = int(accuracy * 60)

        return int(total_time / time_frame_duration)

    def _get_previous_time_frame_worker(self, current_day, time_frame):
        """
        Returns the worker from the previous time frame on the same day, if any.

        Args:
            current_day (str): The current day.
            time_frame (int): The current time frame.

        Returns:
            str or None: The name of the worker, or None if no worker was assigned.
        """
        current_workers = self.schedule.get(current_day, {}).get(time_frame, [])
        previous_time_frame = time_frame - 1
        previous_workers = self.schedule.get(current_day, {}).get(previous_time_frame, [])

        for worker in current_workers:
            if worker in previous_workers:
                return worker
        return None

    def _get_least_used_workers(self):
        """
        Identifies and returns a worker with the minimum usage count within the schedule.

        Returns:
            str or None: The name of a randomly selected worker with the least usage count,
                        or None if no workers are available.
        """
        worker_counts = {}
        least_usage = float('inf')
        least_used_workers = []

        for day, day_info in self.schedule.items():
            for timestamp, workers in day_info.items():
                for worker in workers:
                    count = worker_counts.get(worker, 0) + 1
                    worker_counts[worker] = count

                    if count <= least_usage:
                        least_usage = count
                    if count == least_usage:
                        least_used_workers.append(worker)

        return least_used_workers

    def _get_time_frames_list(self):
        start, end = self._get_working_hours()
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

        return time_frames

    def get_needed_workers_for_time_frame(self, current_time_frame):
        current_start_str, current_end_str = current_time_frame.split('-')
        current_start = self._parse_time(current_start_str)
        current_end = self._parse_time(current_end_str)

        for time_range, workers_needed in self.allocation.items():
            start_str, end_str = time_range.split('-')
            start_time = self._parse_time(start_str)
            end_time = self._parse_time(end_str)

            if (start_time <= current_start < end_time) or (start_time < current_end <= end_time):
                return workers_needed

    def make_schedule(self):
        positions = set([worker.position for worker in self.worker_manager.workers_list])
        days = self.worker_manager.get_days()
        time_frames = self._get_time_frames_list()  # Get the list of time frames for the day

        # Initialize an empty schedule
        self.schedule = {day: {time_frame: [] for time_frame in time_frames} for day in days}

        for day in days:
            for position in positions:
                for index, time_frame in enumerate(time_frames):
                    needed_workers = self.get_needed_workers_for_time_frame(time_frame)
                    # Track workers already assigned to this time frame
                    assigned_workers_for_time_frame = []

                    while len(self.schedule[day][time_frame]) < needed_workers:
                        worker_added = False

                        # Check all conditions to find a suitable worker
                        # 1. Try previous worker
                        previous_worker = self._get_previous_time_frame_worker(day, index)
                        if previous_worker and previous_worker.is_available(day, time_frame) \
                                and previous_worker not in assigned_workers_for_time_frame:
                            self.schedule[day][time_frame].append(previous_worker)
                            assigned_workers_for_time_frame.append(previous_worker)
                            worker_added = True
                            break

                        # 2. Try to prioritize the least used worker
                        if not worker_added:
                            least_used_workers = self._get_least_used_workers()
                            for worker in least_used_workers:
                                if worker.position == position and worker.is_available(day, time_frame) \
                                        and worker not in assigned_workers_for_time_frame:
                                    self.schedule[day][time_frame].append(worker)
                                    assigned_workers_for_time_frame.append(worker)
                                    worker_added = True
                                    break

                        # 3. Take with normal availability
                        if not worker_added:
                            available_workers = self.worker_manager.get_available_workers(day, time_frame)
                            for worker in available_workers:
                                if len(self.schedule[day][time_frame]) < needed_workers:
                                    if worker.position == position and worker not in assigned_workers_for_time_frame:
                                        self.schedule[day][time_frame].append(worker)
                                        assigned_workers_for_time_frame.append(worker)
                                        worker_added = True
                                        break

                        # 4. Check the worse availability
                        if not worker_added:
                            available_workers_if_needed = self.worker_manager.get_available_workers_if_needed(day,
                                                                                                              time_frame)
                            for worker in available_workers_if_needed:
                                if len(self.schedule[day][time_frame]) < needed_workers:
                                    if worker.position == position and worker not in assigned_workers_for_time_frame:
                                        self.schedule[day][time_frame].append(worker)
                                        assigned_workers_for_time_frame.append(worker)
                                        worker_added = True
                                        break

                        # If no worker was added and needed workers are not met, leave the slot as is
                        if not worker_added:
                            break  # Exit the while loop since no more workers can be added

                        # Check if we've met or exceeded the needed number of workers for this time frame
                        if len(assigned_workers_for_time_frame) >= needed_workers:
                            break  # Enough workers have been assigned

                        if len(self.schedule[day][time_frame]) < needed_workers:
                            # Handle the case where not enough workers are available as needed
                            print(
                                f"Not enough workers for {day} in time frame {time_frame}. Needed: {needed_workers},"
                                f" Assigned: {len(self.schedule[day][time_frame])}")

        return self.schedule

    @staticmethod
    def _parse_time(time_str):
        return datetime.strptime(time_str, "%H:%M").time()
