import pytest
from scheduler.variants.scheduler_r import Scheduler_r
from unittest.mock import patch, MagicMock
from worker_manager import Worker_Manager
from worker import Worker


@pytest.fixture
def scheduler_r_instance():
    accuracy = 1
    allocation = {"7:00-10:00": 1, "10:00-14:00": 2}
    return Scheduler_r("R", accuracy=accuracy, allocation=allocation)


def test_init_of_scheduler_r(scheduler_r_instance):
    assert scheduler_r_instance.variant == "R"
    assert scheduler_r_instance.accuracy == 1
    assert scheduler_r_instance.allocation == {"7:00-10:00": 1, "10:00-14:00": 2}
    assert isinstance(scheduler_r_instance.schedule, dict)


# _get_working_hours _________________________________
def test_get_working_hours_no_allocation():
    scheduler = Scheduler_r("R", accuracy=1.0, allocation={})
    assert scheduler._get_working_hours() == (None, None)


def test_get_working_hours_one_allocation():
    scheduler = Scheduler_r("R", accuracy=1.0, allocation={"10:00-14:00": 2})
    assert scheduler._get_working_hours() == ("10:00", "14:00")


def test_get_working_hours_multiple_allocations():
    scheduler = Scheduler_r("R", accuracy=1.0, allocation={"7:00-9:00": 2, "9:00-12:00": 2, "12:00-18:00": 3})
    assert scheduler._get_working_hours() == ("07:00", "18:00")


# _number_of_time_frames_per_day _____________________
def test_number_of_time_frames_per_day_no_time_frames():
    scheduler = Scheduler_r("R", accuracy=1.0, allocation={})
    assert scheduler._number_of_time_frames_per_day() is None


def test_number_of_time_frames_per_day_one_time_frame_one_hour_accuracy():
    scheduler = Scheduler_r("R", accuracy=1.0, allocation={"7:00-8:00": 2})
    assert scheduler._number_of_time_frames_per_day() == 1


def test_number_of_time_frames_per_day_one_time_frame_half_hour_accuracy():
    scheduler = Scheduler_r("R", accuracy=0.5, allocation={"7:00-8:00": 2})
    assert scheduler._number_of_time_frames_per_day() == 2


def test_number_of_time_frames_per_day_one_time_frame_quarter_hour_accuracy():
    scheduler = Scheduler_r("R", accuracy=0.25, allocation={"7:00-8:00": 2})
    assert scheduler._number_of_time_frames_per_day() == 4


# _get_time_frames_list ______________________________
def test_get_time_frames_list_no_allocation():
    scheduler = Scheduler_r("R", accuracy=1.0, allocation={})
    assert scheduler._get_time_frames_list() is None


def test_get_time_frames_list_one_hour_allocation_one_hour_accuracy_one_time_frames():
    scheduler = Scheduler_r("R", accuracy=1.0, allocation={"7:00-8:00": 2})
    assert scheduler._get_time_frames_list() == ["07:00-08:00"]


def test_get_time_frames_list_one_hour_allocation_half_hour_accuracy_multiple_time_frames():
    scheduler = Scheduler_r("R", accuracy=0.5, allocation={"7:00-8:00": 2})
    assert scheduler._get_time_frames_list() == ["07:00-07:30", "07:30-08:00"]


def test_get_time_frames_list_one_hour_allocation_quarter_hour_accuracy_multiple_time_frames():
    scheduler = Scheduler_r("R", accuracy=0.25, allocation={"7:00-8:00": 2})
    assert scheduler._get_time_frames_list() == ["07:00-07:15", "07:15-07:30", "07:30-07:45", "07:45-08:00"]


def test_get_time_frames_list_two_hours_allocation_one_hour_accuracy_multiple_time_frames():
    scheduler = Scheduler_r("R", accuracy=1.0, allocation={"7:00-9:00": 2})
    assert scheduler._get_time_frames_list() == ["07:00-08:00", "08:00-09:00"]


def test_get_time_frames_list_two_hours_allocation_half_hour_accuracy_multiple_time_frames():
    scheduler = Scheduler_r("R", accuracy=0.5, allocation={"7:00-9:00": 2})
    assert scheduler._get_time_frames_list() == ["07:00-07:30", "07:30-08:00", "08:00-08:30", "08:30-09:00"]


# get_needed_workers_for_time_frame __________________
@pytest.mark.parametrize("time_frame, expected_workers", [
    ("9:00-13:00", 2),
    ("10:00-11:00", 2),
    ("9:00-12:00", 2),
    ("13:00-14:00", 3),
    ("15:00-16:00", None),
    ("13:00-15:00", 3),
    (None, None),
])
def test_get_needed_workers_for_time_frame_empty_time_frame(time_frame, expected_workers):
    scheduler = Scheduler_r("R", accuracy=1.0, allocation={"9:00-13:00": 2, "13:00-15:00": 3})
    assert scheduler.get_needed_workers_for_time_frame(time_frame) == expected_workers


def test_get_least_used_workers_no_workers(scheduler_r_instance):
    assert scheduler_r_instance._get_least_used_workers() == []


def test_get_least_used_workers_one_worker(scheduler_r_instance):
    scheduler_r_instance.schedule = {"21.07": {"7:00-8:00": ["Filip"], "8:00-9:00": ["Filip"], "9:00-10:00": ["Filip"],
                                               "10:00-11:00": ["Konrad"], "11:00-12:00": ["Konrad"],
                                               "12:00-13:00": ["Konrad"], "13:00-14:00": ["Ola"]}}
    least_use_workers = scheduler_r_instance._get_least_used_workers()
    assert "Ola" in least_use_workers and "Konrad" not in least_use_workers and "Filip" not in least_use_workers
    assert len(least_use_workers) == 1


def test_get_least_used_workers_equal_usage(scheduler_r_instance):
    scheduler_r_instance.schedule = {"21.07": {"7:00-8:00": ["Filip"], "8:00-9:00": ["Filip"], "9:00-10:00": ["Filip"],
                                               "10:00-11:00": ["Konrad"], "11:00-12:00": ["Konrad"],
                                               "12:00-13:00": ["Konrad"]}}
    least_use_workers = scheduler_r_instance._get_least_used_workers()
    assert "Konrad" not in least_use_workers and "Filip" not in least_use_workers
    assert len(least_use_workers) == 0


def test_get_least_used_workers_two_workers_different_days(scheduler_r_instance):
    scheduler_r_instance.schedule = {"21.07": {"7:00-8:00": ["Filip"], "8:00-9:00": ["Filip"], "9:00-10:00": ["Filip"],
                                               "10:00-11:00": ["Konrad"], "11:00-12:00": ["Konrad"],
                                               "12:00-13:00": ["Konrad"], "13:00-14:00": ["Ola"]},
                                     "22.07": {"7:00-8:00": ["Filip"], "8:00-9:00": ["Filip"], "9:00-10:00": ["Filip"],
                                               "10:00-11:00": ["Konrad"], "11:00-12:00": ["Konrad"],
                                               "12:00-13:00": ["Konrad"], "13:00-14:00": ["Natalia"]}}
    least_use_workers = scheduler_r_instance._get_least_used_workers()
    assert "Ola" in least_use_workers and "Natalia" in least_use_workers and "Konrad" not in least_use_workers \
           and "Filip" not in least_use_workers
    assert len(least_use_workers) == 2


def test_get_previous_time_frame_worker_with_available_workers(scheduler_r_instance):
    mock_worker = MagicMock()
    mock_worker.name = "Filip"
    mock_worker.is_available.return_value = True
    scheduler_r_instance.schedule = {"21.07": {"7:00-8:00": [mock_worker], "8:00-9:00": [mock_worker],
                                               "9:00-10:00": ["Filip"], "10:00-11:00": ["Konrad"],
                                               "11:00-12:00": ["Konrad"], "12:00-13:00": ["Konrad"],
                                               "13:00-14:00": ["Ola"]}}

    with patch.object(scheduler_r_instance, '_get_time_frames_list', return_value=["7:00-8:00", "8:00-9:00",
                                                                                   "9:00-10:00", "10:00-11:00",
                                                                                   "11:00-12:00", "12:00-13:00",
                                                                                   "13:00-14:00"]):
        current_day = "21.07"
        current_time_frame = "8:00-9:00"
        previous_time_frame_worker = scheduler_r_instance._get_previous_time_frame_worker(current_day,
                                                                                          current_time_frame)
        assert previous_time_frame_worker == mock_worker


def test_get_previous_time_frame_worker_with_no_available_workers(scheduler_r_instance):
    mock_worker = MagicMock()
    mock_worker.name = "Filip"
    mock_worker.is_available.return_value = False
    scheduler_r_instance.schedule = {"21.07": {"7:00-8:00": [mock_worker], "8:00-9:00": [mock_worker],
                                               "9:00-10:00": ["Filip"], "10:00-11:00": ["Konrad"],
                                               "11:00-12:00": ["Konrad"], "12:00-13:00": ["Konrad"],
                                               "13:00-14:00": ["Ola"]}}

    with patch.object(scheduler_r_instance, '_get_time_frames_list', return_value=["7:00-8:00", "8:00-9:00",
                                                                                   "9:00-10:00", "10:00-11:00",
                                                                                   "11:00-12:00", "12:00-13:00",
                                                                                   "13:00-14:00"]):
        current_day = "21.07"
        current_time_frame = "8:00-9:00"
        previous_time_frame_worker = scheduler_r_instance._get_previous_time_frame_worker(current_day,
                                                                                          current_time_frame)
        assert previous_time_frame_worker is None


def test_get_previous_time_frame_worker_with_no_previous_time_frame(scheduler_r_instance):
    mock_worker = MagicMock()
    mock_worker.name = "Filip"
    mock_worker.is_available.return_value = False
    scheduler_r_instance.schedule = {"21.07": {"7:00-8:00": [mock_worker], "8:00-9:00": [mock_worker],
                                               "9:00-10:00": ["Filip"], "10:00-11:00": ["Konrad"],
                                               "11:00-12:00": ["Konrad"], "12:00-13:00": ["Konrad"],
                                               "13:00-14:00": ["Ola"]}}

    with patch.object(scheduler_r_instance, '_get_time_frames_list', return_value=["7:00-8:00", "8:00-9:00",
                                                                                   "9:00-10:00", "10:00-11:00",
                                                                                   "11:00-12:00", "12:00-13:00",
                                                                                   "13:00-14:00"]):
        current_day = "21.07"
        current_time_frame = "7:00-8:00"
        previous_time_frame_worker = scheduler_r_instance._get_previous_time_frame_worker(current_day,
                                                                                          current_time_frame)
        assert previous_time_frame_worker is None


# make_schedule() ____________________________________
@pytest.fixture
def scheduler_r_no_worker_needed():
    accuracy = 1
    allocation = {"7:00-10:00": 0}
    scheduler = Scheduler_r("R", accuracy=accuracy, allocation=allocation)

    scheduler.worker_manager = MagicMock()
    scheduler.worker_manager.get_days.return_value = ['21.07']

    return scheduler


def test_make_schedule_no_workers_needed(scheduler_r_no_worker_needed):
    schedule = scheduler_r_no_worker_needed.make_schedule()
    assert schedule.get('21.07', {}).get("9:00-10:00") is None


@pytest.fixture
def mock_worker_manager_one_available_worker():
    worker = MagicMock(spec=Worker, name='Filip')
    worker.name = 'Filip'

    worker_manager = MagicMock(spec=Worker_Manager)
    worker_manager.get_days.return_value = ['21.07']
    worker_manager.get_sorted_workers_by_position_priority.return_value = [worker]
    worker_manager.get_available_workers.return_value = [worker]
    worker_manager.get_available_workers_if_needed = []

    return worker_manager


@pytest.fixture
def scheduler_r_one_worker_needed_for_one_time_frame(mock_worker_manager_one_available_worker):
    accuracy = 1
    allocation = {"7:00-8:00": 1}
    scheduler = Scheduler_r("R", accuracy=accuracy, allocation=allocation)
    scheduler.worker_manager = mock_worker_manager_one_available_worker
    return scheduler


def test_make_schedule_one_worker_needed_one_worker_available(scheduler_r_one_worker_needed_for_one_time_frame):
    schedule = scheduler_r_one_worker_needed_for_one_time_frame.make_schedule()
    assert '21.07' in schedule
    assert '07:00-08:00' in schedule['21.07']
    assert len(schedule['21.07']['07:00-08:00']) == 1
    assert schedule['21.07']['07:00-08:00'][0].name == "Filip"


"""
Write other possible test cases
"""