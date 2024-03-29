from scheduler.scheduler import Scheduler
from datetime import datetime, time, timedelta


class Scheduler_s(Scheduler):
    """
    Class representing a custom scheduler for duty at school.

    """

    def __init__(self, variant: str, time_frames=None, start=None, end=None) -> None:
        super().__init__(variant)
        self.time_frames = time_frames
        self.start = start
        self.end = end
        self.schedule = {}

    def _get_time_frames_list(self):
        time_frames = []

        for day, recesses in self.time_frames.items():
            for recess in recesses:
                time_frame = f"{recess['start']}-{recess['end']}"
                time_frames.append(time_frame)

        return time_frames

    def get_needed_workers_for_time_frame(self, current_time_frame):
        if current_time_frame:
            current_start_str, current_end_str = current_time_frame.split('-')
            current_start = self._parse_time(current_start_str)
            current_end = self._parse_time(current_end_str)

            for day, recesses in self.time_frames.items():
                for recess in recesses:
                    start_time = self._parse_time(recess["start"])
                    end_time = self._parse_time(recess["end"])

                    if (start_time <= current_start < end_time) or (start_time < current_end <= end_time):
                        return recess["allocation"]
        else:
            return None

    def _get_previous_time_frame_worker(self, current_day, current_time_frame):
        sorted_time_frames = self._get_time_frames_list()  # This needs to return time frames in sorted order
        current_index = sorted_time_frames.index(current_time_frame)

        if current_time_frame not in sorted_time_frames:
            raise ValueError(f"Time frame {current_time_frame} not found in schedule.")

        if current_index > 0:
            previous_time_frame = sorted_time_frames[current_index - 1]
            day_schedule = self.schedule.get(current_day, {})

            if previous_time_frame in day_schedule:
                previous_workers = day_schedule[previous_time_frame]
                for worker in previous_workers:
                    if worker.is_available(current_day, current_time_frame):
                        return worker
        return None

    def _get_least_used_workers(self):
        """
        Identifies and returns a worker with the minimum usage count within the schedule.

        Returns:
            str or None: The name of a randomly selected worker with the least usage count,
                        or None if no workers are available.
        """
        worker_counts = {worker: 0 for worker in
                         self.worker_manager.workers_list}  # Initialize all workers with zero usage

        if worker_counts:
            for day_schedule in self.schedule.values():
                for workers in day_schedule.values():
                    for worker in workers:
                        if worker in worker_counts:
                            worker_counts[worker] += 1

            # Check if all workers are used equally
            if len(set(worker_counts.values())) == 1:
                return []

            # Get the worker with the minimum usage count
            least_usage = min(worker_counts.values())
            least_used_workers = [worker for worker, count in worker_counts.items() if count == least_usage]

            return least_used_workers[::-1]
        else:
            return []

    def make_schedule(self):
        days = self.worker_manager.get_days()
        time_frames = self._get_time_frames_list()
        self.schedule = {day: [] for day in days}

        for day in days:
            day_schedule = []  # This will hold all time frame dictionaries for the current day

            for time_frame in time_frames:
                needed_workers = self.get_needed_workers_for_time_frame(time_frame)
                workers_for_time_frame = []  # This will collect workers for the current time frame

                if needed_workers == 0:
                    day_schedule.append({time_frame: ["No worker needed"]})
                    continue

                if len(workers_for_time_frame) < needed_workers:
                    # 1. Try to get previous worker
                    previous_worker = self._get_previous_time_frame_worker(day, time_frame)
                    if previous_worker and previous_worker.is_available(day, time_frame) and \
                            previous_worker not in workers_for_time_frame:
                        workers_for_time_frame.append(previous_worker)

                    # 2. Try to get least used worker
                    least_used_workers = self._get_least_used_workers()
                    for worker in least_used_workers:
                        if len(workers_for_time_frame) < needed_workers and worker not in workers_for_time_frame \
                                and worker.is_available(day, time_frame):
                            workers_for_time_frame.append(worker)

                    # 3. Try to get worker by normal availability
                    available_workers = self.worker_manager.get_available_workers(day, time_frame)
                    for worker in available_workers:
                        if len(workers_for_time_frame) < needed_workers and worker not in workers_for_time_frame:
                            workers_for_time_frame.append(worker)

                    # 4. Try to worker by worse availability
                    if len(workers_for_time_frame) < needed_workers:
                        available_if_needed_workers = self.worker_manager.get_available_workers_if_needed(day,
                                                                                                          time_frame)
                        for worker in available_if_needed_workers:
                            if len(workers_for_time_frame) < needed_workers and worker not in workers_for_time_frame:
                                workers_for_time_frame.append(worker)

                    while len(workers_for_time_frame) < needed_workers:
                        workers_for_time_frame.append("No worker available")

                    day_schedule.append({time_frame: workers_for_time_frame})

            self.schedule[day] = day_schedule

        return self.schedule

    def _get_working_hours(self):
        pass
