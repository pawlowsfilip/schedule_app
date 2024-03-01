from scheduler.scheduler import Scheduler
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
        self.allocation = allocation  # {"7:00-10:00": 1, ...}
        self.variant = variant
        self.schedule = {}

    def _number_of_time_frames_per_day(self):
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
        time_frame_duration = int(self.accuracy * 60)

        return int(total_time / time_frame_duration)

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

    def make_schedule(self):
        days = self.worker_manager.get_days()
        time_frames = self._get_time_frames_list()

        # Initialize an empty schedule
        self.schedule = {day: {time_frame: [] for time_frame in time_frames} for day in days}

        for day in days:
            for time_frame in time_frames:
                needed_workers = self.get_needed_workers_for_time_frame(time_frame)

                if needed_workers == 0:
                    continue  # Skip if no workers are needed for this time frame

                # 1. Sort workers based on the priorities
                sorted_workers = self.worker_manager.get_sorted_workers_by_position_priority()

                for worker in sorted_workers:
                    # Skip if the time frame already has the needed workers
                    if len(self.schedule[day][time_frame]) >= needed_workers:
                        break

                    # 2. Check if previous worker on that position is still available
                    if worker == self._get_previous_time_frame_worker(day, time_frame) and worker.is_available(
                            day, time_frame):
                        if worker not in self.schedule[day][time_frame]:
                            self.schedule[day][time_frame].append(worker)
                            continue

                    # 3. Check the least used worker on that position is still available
                    least_used_workers = self._get_least_used_workers()
                    for least_used_worker in least_used_workers:
                        if least_used_worker.position == worker.position and least_used_worker.is_available(
                                day, time_frame):
                            if least_used_worker not in self.schedule[day][time_frame]:
                                self.schedule[day][time_frame].append(least_used_worker)
                                break

                    # 4. Check the available workers on that position
                    if worker.is_available(day, time_frame) and worker not in self.schedule[day][time_frame]:
                        self.schedule[day][time_frame].append(worker)
                        continue

                    # 5. Check the available if needed on that position.
                    if worker.is_available_if_needed(day, time_frame) and worker not in self.schedule[day][time_frame]:
                        self.schedule[day][time_frame].append(worker)
                        continue

        # Handle cases where not enough workers are available
        for day, day_schedule in self.schedule.items():
            for time_frame, workers in day_schedule.items():
                while len(workers) < self.get_needed_workers_for_time_frame(time_frame):
                    workers.append("No worker available")

        return self.schedule
