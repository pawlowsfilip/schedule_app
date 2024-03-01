from worker_manager import Worker_Manager
from worker import Worker
from datetime import datetime, timedelta
from abc import ABC, abstractmethod


class Scheduler(ABC):
    def __init__(self, variant):
        worker1 = Worker('Filip', {'21.07': '8:00-10:00'}, {}, 'Manager')
        worker2 = Worker('Natalia', {'21.07': '8:00-10:00'}, {}, 'Regular')
        worker3 = Worker('Ola', {'21.07': '8:00-9:00'}, {'21.07': '10:00-14:00'}, 'Student')
        worker4 = Worker('Kondziu', {'21.07': '10:00-14:00'}, {'21.07': '10:00-14:00'}, 'Student')
        wm1 = Worker_Manager(worker1, worker2, worker3, worker4)
        wm1.set_position_priorities({'Manager': 1, 'Regular': 2, "Student": 3})

        self.variant = variant
        self.schedule = {}
        # self.worker_manager = Worker_Manager()
        self.worker_manager = wm1

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

    def _get_previous_time_frame_worker(self, current_day, current_time_frame):
        sorted_time_frames = self._get_time_frames_list()  # This needs to return time frames in sorted order
        current_index = sorted_time_frames.index(current_time_frame)

        if current_index > 0:
            previous_time_frame = sorted_time_frames[current_index - 1]
            previous_workers = self.schedule.get(current_day, {}).get(previous_time_frame, [])

            for worker in previous_workers:
                if worker.is_available(current_day, current_time_frame):
                    return worker

        return None

    @staticmethod
    def _parse_time(time_str):
        return datetime.strptime(time_str, "%H:%M").time()

    @abstractmethod
    def _get_time_frames_list(self):
        """Generates a list of time frames for the day."""
        pass
