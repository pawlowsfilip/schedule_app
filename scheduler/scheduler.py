from worker_manager import Worker_Manager
from datetime import datetime
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class Scheduler(ABC):
    def __init__(self, variant):
        try:
            self.variant = variant
            self.schedule = {}
            self.worker_manager = Worker_Manager()
            logger.debug(f"Scheduler initialized with variant {variant}")
        except Exception as e:
            logger.error(f"Error during initialization of Scheduler: {e}")
            raise

    @abstractmethod
    def _get_previous_time_frame_worker(self, current_day, current_time_frame):
        pass

    @abstractmethod
    def _get_least_used_workers(self):
        pass

    @abstractmethod
    def _get_time_frames_list(self):
        pass

    @abstractmethod
    def make_schedule(self):
        pass

    @abstractmethod
    def _get_working_hours(self):
        pass

    @abstractmethod
    def get_needed_workers_for_time_frame(self, day, current_time_frame):
        pass

    @staticmethod
    def _parse_time(time_str):
        try:
            time_obj = datetime.strptime(time_str, "%H:%M").time()
            logger.debug(f"Parsed time string {time_str} into time object {time_obj}")
            return time_obj
        except ValueError as e:
            logger.error(f"Error parsing time string {time_str}: {e}")
            raise
