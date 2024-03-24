import pytest
from scheduler.variants.scheduler_s import Scheduler_s
from unittest.mock import MagicMock
from worker_manager import Worker_Manager
from worker import Worker

"""
_get_previous_time_frame_worker()
├── Previous Time Frame Has No Workers - DONE
├── Previous Worker Is Not Available For Current Time Frame - DONE
├── Previous Worker Is Available For Current Time Frame - DONE
├── Multiple Workers in Previous Time Frame, One Available
├── No Previous Time Frame
├── Invalid Time Frame
├── Correct Handling of Different Days
└── Workers Available in Non-Consecutive Previous Time Frame
"""

# Previous Time Frame Has No Workers _______________________________________________________________
@pytest.fixture
def mock_worker_manager_no_workers():
    worker_manager = MagicMock(spec=Worker_Manager)
    worker_manager.get_days.return_value = ["21.07"]
    worker_manager.get_sorted_workers_by_position_priority.return_value = []
    return worker_manager


@pytest.fixture
def scheduler_s_no_workers(mock_worker_manager_no_workers):
    scheduler = Scheduler_s("S", time_frames={"21.07": [{"start": "8:00", "end": "8:15", "allocation": 1},
                                                        {"start": "9:00", "end": "9:15", "allocation": 2}]})
    scheduler.worker_manager = mock_worker_manager_no_workers
    scheduler.schedule = {
        "21.07": {"8:00-8:15": []
                  }
    }
    scheduler._get_time_frames_list = MagicMock(return_value=["08:00-08:15", "09:00-09:15"])
    return scheduler

def test_get_previous_time_frame_worker_no_workers(scheduler_s_no_workers):
    previous_worker = scheduler_s_no_workers._get_previous_time_frame_worker("21.07", "09:00-09:15")

    assert previous_worker is None


# Previous Worker Is Not Available For Current Time Frame __________________________________________
@pytest.fixture
def mock_worker_manager_previous_not_available():
    worker1 = MagicMock(spec=Worker, name='Filip')
    worker1.name = 'Filip'
    worker1.position = 'Student'
    worker1.is_available.side_effect = lambda day, time_frame: time_frame in ["08:00-08:15"]
    worker1.is_available_if_needed.return_value = False

    worker2 = MagicMock(spec=Worker, name='Konrad')
    worker2.name = 'Konrad'
    worker2.position = 'Student'
    worker2.is_available.side_effect = lambda day, time_frame: time_frame in ["09:00-09:15"]
    worker2.is_available_if_needed.return_value = False

    worker_manager = MagicMock(spec=Worker_Manager)
    worker_manager.get_days.return_value = ['21.07']
    worker_manager.get_sorted_workers_by_position_priority.return_value = [worker1, worker2]

    worker_manager.workers_list = [worker1, worker2]

    return worker_manager


@pytest.fixture
def scheduler_s_previous_not_available(mock_worker_manager_previous_not_available):
    scheduler = Scheduler_s("S", time_frames={"21.07": [{"start": "8:00", "end": "8:15", "allocation": 1},
                                                        {"start": "9:00", "end": "9:15", "allocation": 1}]})
    scheduler.worker_manager = mock_worker_manager_previous_not_available
    mock_worker1, mock_worker2 = mock_worker_manager_previous_not_available.workers_list
    scheduler.schedule = {
        "21.07": {"8:00-8:15": [mock_worker1]
                  }
    }
    scheduler._get_time_frames_list = MagicMock(return_value=["08:00-08:15", "09:00-09:15"])
    return scheduler


def test_get_previous_time_frame_worker_previous_not_available(scheduler_s_previous_not_available):
    previous_worker = scheduler_s_previous_not_available._get_previous_time_frame_worker("21.07", "09:00-09:15")
    assert previous_worker is None

# Previous Worker Is Available For Current Time Frame ______________________________________________
@pytest.fixture
def mock_worker_manager_previous_available():
    worker1 = MagicMock(spec=Worker, name='Filip')
    worker1.name = 'Filip'
    worker1.position = 'Student'
    worker1.is_available.side_effect = lambda day, time_frame: time_frame in ["08:00-08:15", "09:00-09:15"]
    worker1.is_available_if_needed.return_value = False

    worker2 = MagicMock(spec=Worker, name='Konrad')
    worker2.name = 'Konrad'
    worker2.position = 'Student'
    worker2.is_available.side_effect = lambda day, time_frame: time_frame in ["08:00-08:15", "09:00-09:15"]
    worker2.is_available_if_needed.return_value = False

    worker_manager = MagicMock(spec=Worker_Manager)
    worker_manager.get_days.return_value = ['21.07']
    worker_manager.get_sorted_workers_by_position_priority.return_value = [worker1, worker2]

    worker_manager.workers_list = [worker1, worker2]

    return worker_manager


@pytest.fixture
def scheduler_s_previous_available(mock_worker_manager_previous_available):
    scheduler = Scheduler_s("S", time_frames={"21.07": [{"start": "8:00", "end": "8:15", "allocation": 1},
                                                        {"start": "9:00", "end": "9:15", "allocation": 2}]})
    scheduler.worker_manager = mock_worker_manager_previous_available
    mock_worker1, mock_worker2 = mock_worker_manager_previous_available.workers_list
    scheduler.schedule = {
        "21.07": {"08:00-08:15": [mock_worker1],
                  "09:00-09:15": [mock_worker1, mock_worker2]
                  }
    }
    scheduler._get_time_frames_list = MagicMock(return_value=["08:00-08:15", "09:00-09:15"])
    return scheduler


def test_get_previous_time_frame_worker_previous_available(scheduler_s_previous_available):
    previous_worker = scheduler_s_previous_available._get_previous_time_frame_worker("21.07", "09:00-09:15")
    assert previous_worker.name == "Filip"

