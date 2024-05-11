from scheduler.scheduler import Scheduler
from datetime import datetime, timedelta
from worker import Worker


class Scheduler_r(Scheduler):
    """
    Class representing a custom scheduler for restaurants.

    Args:
        accuracy (float): Desired accuracy of the scheduling process (accuracy of 1hr, 0.5hr, 0.25hr etc).
        allocation (dict): Dictionary representing worker allocations as {"start_time-end_time": number_of_workers}.
        variant (str): Variant identifier for the scheduling algorithm.
    """

    def __init__(self, variant: str, accuracy=None, allocation=None) -> None:
        super().__init__(variant)
        self.accuracy = accuracy
        self.allocation = allocation
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
        print(self.allocation)
        print(self.allocation.keys())

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
                except ValueError:
                    print(f"Invalid time range: {time_range}")

        earliest_start_str = earliest_start.strftime('%H:%M') if earliest_start else None
        latest_end_str = latest_end.strftime('%H:%M') if latest_end else None

        return earliest_start_str, latest_end_str

    def _number_of_time_frames_per_day(self):
        """
        Calculates the number of time frames per day based on the desired accuracy.

        Args:
            accuracy (float): Desired accuracy of the scheduling process (accuracy of 1hr, 0.5hr, 0.25hr etc).

        Returns:
            int: The number of time frames per day.
        """
        start, end = self._get_working_hours()
        if start and end:
            # having the strptime because it is easier to subtract end from start
            start_time = datetime.strptime(start, '%H:%M')
            end_time = datetime.strptime(end, '%H:%M')

            # calculate the time frame in minutes
            total_time = (end_time - start_time).total_seconds() / 60
            time_frame_duration = int(self.accuracy * 60)

            return int(total_time / time_frame_duration)
        else:
            return None

    def _get_time_frames_list(self):
        start, end = self._get_working_hours()
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

            return time_frames
        else:
            return None

    def get_needed_workers_for_time_frame(self, day, current_time_frame):
        if not current_time_frame:
            return 0

        current_start_str, current_end_str = current_time_frame.split('-')
        current_start = self._parse_time(current_start_str)
        current_end = self._parse_time(current_end_str)

        if day in self.allocation:
            for time_frame, workers_needed in self.allocation[day].items():
                start_str, end_str = time_frame.split('-')
                start_time = self._parse_time(start_str)
                end_time = self._parse_time(end_str)

                if (start_time <= current_start < end_time) or (start_time < current_end <= end_time):
                    return workers_needed

        return 0

    def _get_least_used_workers(self):
        """
        Identifies and returns a list of workers with the minimum usage count within the schedule.
        If all workers have the same usage count, returns an empty list because they are equally used.

        Returns:
            list: A list of worker objects with the least usage count, or an empty list if no workers are available or all are equally used.
        """
        worker_counts = {worker: 0 for worker in
                         self.worker_manager.workers_list}  # Initialize all workers with zero usage
        if worker_counts:
            # Count usage for each worker
            for day_info in self.schedule.values():
                for workers in day_info.values():
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

    def _get_previous_time_frame_worker(self, current_day, current_time_frame):
        sorted_time_frames = self._get_time_frames_list()  # This needs to return time frames in sorted order
        current_index = sorted_time_frames.index(current_time_frame)

        if current_index > 0:
            previous_time_frame = sorted_time_frames[current_index - 1]
            previous_workers = self.schedule.get(current_day, {}).get(previous_time_frame, [])

            for worker in previous_workers:
                if not isinstance(worker, Worker):
                    continue
                else:
                    if worker.is_available(current_day, current_time_frame):
                        return worker
        return None

    def make_schedule(self):
        days = self.worker_manager.get_days()
        time_frames = self._get_time_frames_list()

        # Initialize an empty schedule
        self.schedule = {day: {time_frame: [] for time_frame in time_frames} for day in days}

        for day in days:
            for time_frame in time_frames:
                print('time frame', time_frame)
                needed_workers = self.get_needed_workers_for_time_frame(day, time_frame)

                if needed_workers == 0:
                    continue  # Skip if no workers are needed for this time frame

                workers_for_time_frame = []

                # 1. Sort workers based on the priorities
                sorted_workers = self.worker_manager.get_sorted_workers_by_position_priority()

                # Reverse the order, because the higher value, the lower position worker has.
                for worker in sorted_workers[::-1]:
                    # Skip if the time frame already has the needed workers
                    if len(workers_for_time_frame) >= needed_workers:
                        break

                    # 2. Check if previous worker on that position is still available
                    if worker == self._get_previous_time_frame_worker(day, time_frame) and worker.is_available(
                            day, time_frame):
                        if worker not in workers_for_time_frame:
                            workers_for_time_frame.append(worker)
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
                                break
                    # Skip if the time frame already has the needed workers
                    if len(self.schedule[day][time_frame]) >= needed_workers:
                        break

                    # 4. Check the available workers on that position
                    if worker.is_available(day, time_frame) and worker not in workers_for_time_frame:
                        workers_for_time_frame.append(worker)
                        continue

                    # Skip if the time frame already has the needed workers
                    if len(workers_for_time_frame) >= needed_workers:
                        break

                    # 5. Check the available if needed on that position.
                    if worker.is_available_if_needed(day, time_frame) and worker not in workers_for_time_frame:
                        workers_for_time_frame.append(worker)
                        continue

                    # Skip if the time frame already has the needed workers
                    if len(self.schedule[day][time_frame]) >= needed_workers:
                        break

        # # Handle cases where not enough workers are available
        # for day, day_schedule in self.schedule.items():
        #     for time_frame, workers in day_schedule.items():
        #         while len(workers) < self.get_needed_workers_for_time_frame(day, time_frame):
        #             workers.append("No worker available")

                while len(workers_for_time_frame) < needed_workers:
                    workers_for_time_frame.append("NO WORKER")

                if all(worker == "NO WORKER" for worker in workers_for_time_frame):
                    workers_for_time_frame = ["NO WORKER AVAILABLE"]

                self.schedule[day][time_frame] = workers_for_time_frame

        return self.schedule
