from unittest.mock import patch

import pytest
from datetime import time
from scheduler.scheduler import Scheduler
from worker import Worker
from worker_manager import Worker_Manager


class ConcreteScheduler(Scheduler):
    """A concrete implementation of Scheduler for testing purposes."""

    def _get_previous_time_frame_worker(self, current_day, current_time_frame):
        pass

    def _get_least_used_workers(self):
        pass

    def _get_time_frames_list(self):
        pass

    def make_schedule(self):
        pass

    def _get_working_hours(self):
        pass

    def get_needed_workers_for_time_frame(self, current_time_frame):
        pass


@pytest.fixture
def worker_manager_with_workers():
    w1 = Worker("John Doe", {'21.07': '9:00-17:00'})
    w2 = Worker("Doe John", {'22.07': '9:00-17:00'})
    wm = Worker_Manager(w1, w2)
    return wm


def test_scheduler_initialization_r(worker_manager_with_workers):
    variant = "R"

    with patch('scheduler.scheduler.Worker_Manager', return_value=worker_manager_with_workers):
        scheduler = ConcreteScheduler(variant=variant)
        assert scheduler.variant == variant
        assert isinstance(scheduler.schedule, dict)


def test_scheduler_initialization_s(worker_manager_with_workers):
    variant = "S"

    with patch('scheduler.scheduler.Worker_Manager', return_value=worker_manager_with_workers):
        scheduler = ConcreteScheduler(variant=variant)
        assert scheduler.variant == variant
        assert isinstance(scheduler.schedule, dict)


@pytest.mark.parametrize("time_str, expected", [
    ("00:00", time(0, 0)),
    ("21:37", time(21, 37)),
    ("12:37", time(12, 37)),
    ("01:01", time(1, 1)),
])
def test_parse_time(time_str, expected):
    assert Scheduler._parse_time(time_str) == expected
