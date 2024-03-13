import pytest
from scheduler.variants.scheduler_r import Scheduler_r
from unittest.mock import patch, MagicMock


@pytest.fixture
def scheduler_r_instance():
    accuracy = 1
    allocation = {"7:00-10:00": 1, "10:00-14:00": 2}
    return Scheduler_r("R", accuracy=accuracy, allocation=allocation)


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