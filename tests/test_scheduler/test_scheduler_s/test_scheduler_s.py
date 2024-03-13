from scheduler.scheduler import Scheduler
from scheduler.variants.scheduler_s import Scheduler_s
import pytest
from unittest.mock import Mock, create_autospec, patch
from worker_manager import Worker_Manager
from worker import Worker

# global mock workers
mock_worker_1 = Mock(spec=Worker, name="Filip")
mock_worker_1.is_available.return_value = True

mock_worker_2 = Mock(spec=Worker, name="Konrad")
mock_worker_2.is_available.return_value = True


def test_init_with_all_arguments():
    scheduler = Scheduler_s("S", {'21.07': [{"start": "8:00", "end": "8:15", "allocation": 1},
                                            {"start": "9:00", "end": "9:15", "allocation": 2}]}, "7:00", "14:00")
    assert scheduler.time_frames == {'21.07': [{"start": "8:00", "end": "8:15", "allocation": 1},
                                               {"start": "9:00", "end": "9:15", "allocation": 2}]}
    assert scheduler.variant == "S"


def test_get_time_frames_list_for_one_time_frame():
    scheduler = Scheduler_s("S", {'21.07': [{"start": "8:00", "end": "8:15", "allocation": 1}]}, "7:00", "14:00")
    assert len(scheduler._get_time_frames_list()) == 1


def test_get_time_frames_list_for_more_than_one_time_frame():
    scheduler = Scheduler_s("S", {'21.07': [{"start": "8:00", "end": "8:15", "allocation": 1},
                                            {"start": "9:00", "end": "9:15", "allocation": 2}]}, "7:00", "14:00")
    assert len(scheduler._get_time_frames_list()) == 2


@pytest.fixture
def mock_worker_manager():
    wm = Mock(spec=Worker_Manager)
    wm.get_days.return_value = ["21.07"]
    wm.get_available_workers.return_value = [mock_worker_1, mock_worker_2]
    wm.get_available_workers_if_needed.return_value = [mock_worker_1]
    return wm


@pytest.fixture
def setup_scheduler(mock_worker_manager):
    scheduler = Scheduler_s("S", time_frames={"21.07": [{"start": "8:00", "end": "8:15", "allocation": 1},
                                                        {"start": "9:00", "end": "9:15", "allocation": 2}]},
                            start="7:00", end="14:00")
    scheduler.worker_manager = mock_worker_manager
    return scheduler


def test_make_schedule_with_one_worker(setup_scheduler):
    # Directly use the setup_scheduler fixture, which is already a Scheduler_s instance
    expected_schedule = {"21.07": [{"8:00-8:15": [mock_worker_1]},
                                   {"9:00-9:15": [mock_worker_1, mock_worker_2]}]}  # Expected to use the worker's name

    actual_schedule = setup_scheduler.make_schedule()

    # Assert the expected and actual schedules match
    assert actual_schedule == expected_schedule
