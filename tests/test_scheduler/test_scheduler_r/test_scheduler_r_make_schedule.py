import pytest
from scheduler.variants.scheduler_r import Scheduler_r
from unittest.mock import patch, MagicMock
from worker_manager import Worker_Manager
from worker import Worker

"""
Test cases tree:

make_schedule()
├── No workers needed for any time frame - DONE
├── Workers needed for specific time frames - 
│   ├── Only one worker needed and one is available - DONE
│   │   ├── Worker is available normally - DONE
│   │   └── Worker is available "if needed" - DONE
│   ├── More than one worker needed and sufficient workers are available - DONE
│   │   ├── All workers are available normally - DONE
│   │   └── Some workers are available "if needed" - DONE
│   ├── Workers needed but no workers are available - DONE
│   │   ├── No workers available normally and none "if needed" - DONE
│   └── Workers needed, but less than needed are available - DONE
│       ├── Fewer workers available than needed, indicates "No worker available" - DONE
│       └── Workers are available "if needed", Schedule indicates "No worker available" - DONE
└── Workers needed with various priorities
    ├── Workers sorted by position priority - DONE
    │   ├── Highest priority workers are assigned first - DONE
    │   └── Lower priority workers are assigned if higher are unavailable - DONE
    └── Checking for previous and least used workers
        ├── Previous time frame worker is re-utilized if available - DONE
        ├── Least used worker is prioritized if previous not available - DONE
        └── New worker is added if neither previous nor least used is suitable - DONE
"""


# No workers needed for any time frame _________________________________________________________________________________
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


# Workers needed for specific time frames ______________________________________________________________________________
# Only one worker needed and one is available ______________________________________________________
# Worker is available normally _________________________________________________
@pytest.fixture
def mock_worker_manager_one_worker_normal_availability():
    worker1 = MagicMock(spec=Worker, name='Filip')
    worker1.name = 'Filip'
    worker1.position = 'Student'
    worker1.is_available.return_value = True
    worker1.is_available_if_needed.return_value = False

    worker_manager = MagicMock(spec=Worker_Manager)
    worker_manager.get_days.return_value = ['21.07']
    worker_manager.get_sorted_workers_by_position_priority.return_value = [worker1]

    worker_manager.workers_list = [worker1]

    return worker_manager


@pytest.fixture
def scheduler_r_one_worker_needed_for_one_time_frame_normal_availability(
        mock_worker_manager_one_worker_normal_availability):
    accuracy = 1
    allocation = {"7:00-8:00": 1}
    scheduler = Scheduler_r("R", accuracy=accuracy, allocation=allocation)
    scheduler.worker_manager = mock_worker_manager_one_worker_normal_availability
    return scheduler


def test_make_schedule_one_worker_needed_for_one_time_frame_normal_availability(
        scheduler_r_one_worker_needed_for_one_time_frame_normal_availability):
    schedule = scheduler_r_one_worker_needed_for_one_time_frame_normal_availability.make_schedule()
    assert '21.07' in schedule
    assert len(schedule['21.07']['07:00-08:00']) == 1
    assert schedule['21.07']['07:00-08:00'][0].name == "Filip"


# Worker is available "if needed" ______________________________________________
@pytest.fixture
def mock_worker_manager_one_worker_worse_availability():
    worker1 = MagicMock(spec=Worker, name='Filip')
    worker1.name = 'Filip'
    worker1.position = 'Student'
    worker1.is_available.return_value = False
    worker1.is_available_if_needed.return_value = True

    worker_manager = MagicMock(spec=Worker_Manager)
    worker_manager.get_days.return_value = ['21.07']
    worker_manager.get_sorted_workers_by_position_priority.return_value = [worker1]

    worker_manager.workers_list = [worker1]

    return worker_manager


@pytest.fixture
def scheduler_r_one_worker_needed_for_one_time_frame_one_worker_worse_availability(
        mock_worker_manager_one_worker_worse_availability):
    accuracy = 1
    allocation = {"7:00-8:00": 1}
    scheduler = Scheduler_r("R", accuracy=accuracy, allocation=allocation)
    scheduler.worker_manager = mock_worker_manager_one_worker_worse_availability
    return scheduler


def test_make_schedule_two_workers_needed_for_one_time_frame_one_worker_worse_availability(
        scheduler_r_one_worker_needed_for_one_time_frame_one_worker_worse_availability):
    schedule = scheduler_r_one_worker_needed_for_one_time_frame_one_worker_worse_availability.make_schedule()
    assert '21.07' in schedule
    assert len(schedule['21.07']['07:00-08:00']) == 1
    assert schedule['21.07']['07:00-08:00'][0].name == "Filip"


# More than one worker needed and sufficient workers are available _________________________________
# All workers are available normally ___________________________________________
@pytest.fixture
def mock_worker_manager_two_workers_normal_availability():
    worker1 = MagicMock(spec=Worker, name='Filip')
    worker1.name = 'Filip'
    worker1.position = 'Student'
    worker1.is_available.return_value = True
    worker1.is_available_if_needed.return_value = False

    worker2 = MagicMock(spec=Worker, name='Konrad')
    worker2.name = 'Konrad'
    worker2.position = 'Student'
    worker2.is_available.return_value = True
    worker2.is_available_if_needed.return_value = False

    worker_manager = MagicMock(spec=Worker_Manager)
    worker_manager.get_days.return_value = ['21.07']
    worker_manager.get_sorted_workers_by_position_priority.return_value = [worker1, worker2]

    worker_manager.workers_list = [worker1, worker2]

    return worker_manager


@pytest.fixture
def scheduler_r_two_workers_needed_for_one_time_frame_normal_availability(
        mock_worker_manager_two_workers_normal_availability):
    accuracy = 1
    allocation = {"7:00-8:00": 2}
    scheduler = Scheduler_r("R", accuracy=accuracy, allocation=allocation)
    scheduler.worker_manager = mock_worker_manager_two_workers_normal_availability
    return scheduler


def test_make_schedule_two_workers_needed_for_one_time_frame_normal_availability(
        scheduler_r_two_workers_needed_for_one_time_frame_normal_availability):
    schedule = scheduler_r_two_workers_needed_for_one_time_frame_normal_availability.make_schedule()
    assert '21.07' in schedule
    assert len(schedule['21.07']['07:00-08:00']) == 2
    assert schedule['21.07']['07:00-08:00'][0].name == "Konrad"
    assert schedule['21.07']['07:00-08:00'][1].name == "Filip"


# Some workers are available "if needed" _______________________________________
@pytest.fixture
def mock_worker_manager_two_workers_two_workers_worse_availability():
    worker1 = MagicMock(spec=Worker, name='Filip')
    worker1.name = 'Filip'
    worker1.position = 'Student'
    worker1.is_available.return_value = False
    worker1.is_available_if_needed.return_value = True

    worker2 = MagicMock(spec=Worker, name='Konrad')
    worker2.name = 'Konrad'
    worker2.position = 'Student'
    worker2.is_available.return_value = False
    worker2.is_available_if_needed.return_value = True

    worker_manager = MagicMock(spec=Worker_Manager)
    worker_manager.get_days.return_value = ['21.07']
    worker_manager.get_sorted_workers_by_position_priority.return_value = [worker1, worker2]

    worker_manager.workers_list = [worker1, worker2]

    return worker_manager


@pytest.fixture
def scheduler_r_two_worker_needed_for_one_time_frame_two_workers_worse_availability(
        mock_worker_manager_two_workers_two_workers_worse_availability):
    accuracy = 1
    allocation = {"7:00-8:00": 2}
    scheduler = Scheduler_r("R", accuracy=accuracy, allocation=allocation)
    scheduler.worker_manager = mock_worker_manager_two_workers_two_workers_worse_availability
    return scheduler


def test_make_schedule_two_worker_needed_for_one_time_frame_two_workers_worse_availability(
        scheduler_r_two_worker_needed_for_one_time_frame_two_workers_worse_availability):
    schedule = scheduler_r_two_worker_needed_for_one_time_frame_two_workers_worse_availability.make_schedule()
    assert '21.07' in schedule
    assert len(schedule['21.07']['07:00-08:00']) == 2
    assert schedule['21.07']['07:00-08:00'][0].name == "Konrad"
    assert schedule['21.07']['07:00-08:00'][1].name == "Filip"


# Workers needed but no workers are available ______________________________________________________
# No workers available normally and none "if needed" ___________________________
@pytest.fixture
def mock_worker_manager_no_workers_normal_availability_and_worse():
    worker1 = MagicMock(spec=Worker, name='Filip')
    worker1.name = 'Filip'
    worker1.position = 'Student'
    worker1.is_available.return_value = False
    worker1.is_available_if_needed.return_value = False

    worker2 = MagicMock(spec=Worker, name='Konrad')
    worker2.name = 'Konrad'
    worker2.position = 'Student'
    worker2.is_available.return_value = False
    worker2.is_available_if_needed.return_value = False

    worker_manager = MagicMock(spec=Worker_Manager)
    worker_manager.get_days.return_value = ['21.07']
    worker_manager.get_sorted_workers_by_position_priority.return_value = [worker1, worker2]

    worker_manager.workers_list = [worker1, worker2]

    return worker_manager


@pytest.fixture
def scheduler_r_two_workers_needed_no_workers_normal_availability_and_worse(
        mock_worker_manager_no_workers_normal_availability_and_worse):
    accuracy = 1
    allocation = {"7:00-8:00": 2}
    scheduler = Scheduler_r("R", accuracy=accuracy, allocation=allocation)
    scheduler.worker_manager = mock_worker_manager_no_workers_normal_availability_and_worse
    return scheduler


def test_make_schedule_two_workers_needed_no_workers_normal_availability_and_worse(
        scheduler_r_two_workers_needed_no_workers_normal_availability_and_worse):
    schedule = scheduler_r_two_workers_needed_no_workers_normal_availability_and_worse.make_schedule()
    assert '21.07' in schedule
    assert len(schedule['21.07']['07:00-08:00']) == 2
    assert schedule['21.07']['07:00-08:00'][0] == "No worker available"
    assert schedule['21.07']['07:00-08:00'][1] == "No worker available"


# Workers needed, but less than needed are available _______________________________________________
# Fewer workers available than needed, indicates "No worker available" __________
@pytest.fixture
def mock_worker_manager_two_workers_one_worker_normal_availability():
    worker1 = MagicMock(spec=Worker, name='Filip')
    worker1.name = 'Filip'
    worker1.position = 'Student'
    worker1.is_available.return_value = False
    worker1.is_available_if_needed.return_value = False

    worker2 = MagicMock(spec=Worker, name='Konrad')
    worker2.name = 'Konrad'
    worker2.position = 'Student'
    worker2.is_available.return_value = True
    worker2.is_available_if_needed.return_value = False

    worker_manager = MagicMock(spec=Worker_Manager)
    worker_manager.get_days.return_value = ['21.07']
    worker_manager.get_sorted_workers_by_position_priority.return_value = [worker1, worker2]

    worker_manager.workers_list = [worker1, worker2]

    return worker_manager


@pytest.fixture
def scheduler_r_two_worker_needed_for_one_time_frame_one_worker_normal_availability(
        mock_worker_manager_two_workers_one_worker_normal_availability):
    accuracy = 1
    allocation = {"7:00-8:00": 2}
    scheduler = Scheduler_r("R", accuracy=accuracy, allocation=allocation)
    scheduler.worker_manager = mock_worker_manager_two_workers_one_worker_normal_availability
    return scheduler


def test_scheduler_r_two_worker_needed_for_one_time_frame_one_worker_normal_availability(
        scheduler_r_two_worker_needed_for_one_time_frame_one_worker_normal_availability):
    schedule = scheduler_r_two_worker_needed_for_one_time_frame_one_worker_normal_availability.make_schedule()
    assert '21.07' in schedule
    assert len(schedule['21.07']['07:00-08:00']) == 2
    assert schedule['21.07']['07:00-08:00'][0].name == "Konrad"
    assert schedule['21.07']['07:00-08:00'][1] == "No worker available"


# Workers are available "if needed", Schedule indicates "No worker available" __
@pytest.fixture
def mock_worker_manager_two_workers_one_worker_worse_availability():
    worker1 = MagicMock(spec=Worker, name='Filip')
    worker1.name = 'Filip'
    worker1.position = 'Student'
    worker1.is_available.return_value = False
    worker1.is_available_if_needed.return_value = False

    worker2 = MagicMock(spec=Worker, name='Konrad')
    worker2.name = 'Konrad'
    worker2.position = 'Student'
    worker2.is_available.return_value = False
    worker2.is_available_if_needed.return_value = True

    worker_manager = MagicMock(spec=Worker_Manager)
    worker_manager.get_days.return_value = ['21.07']
    worker_manager.get_sorted_workers_by_position_priority.return_value = [worker1, worker2]

    worker_manager.workers_list = [worker1, worker2]

    return worker_manager


@pytest.fixture
def scheduler_r_two_workers_needed_for_one_time_frame_one_worker_worse_availability(
        mock_worker_manager_two_workers_one_worker_worse_availability):
    accuracy = 1
    allocation = {"7:00-8:00": 2}
    scheduler = Scheduler_r("R", accuracy=accuracy, allocation=allocation)
    scheduler.worker_manager = mock_worker_manager_two_workers_one_worker_worse_availability
    return scheduler


def test_make_schedule_two_worker_needed_for_one_time_frame_one_worker_worse_availability(
        scheduler_r_two_workers_needed_for_one_time_frame_one_worker_worse_availability):
    schedule = scheduler_r_two_workers_needed_for_one_time_frame_one_worker_worse_availability.make_schedule()
    assert '21.07' in schedule
    assert len(schedule['21.07']['07:00-08:00']) == 2
    assert schedule['21.07']['07:00-08:00'][0].name == "Konrad"
    assert schedule['21.07']['07:00-08:00'][1] == "No worker available"


# Workers needed with various priorities _______________________________________________________________________________
# Workers sorted by position priority ______________________________________________________________
# Highest priority workers are assigned first __________________________________
@pytest.fixture
def mock_worker_manager_three_workers_normal_availability_sorted_priority():
    worker1 = MagicMock(spec=Worker, name='Filip')
    worker1.name = 'Filip'
    worker1.position = 'CEO'
    worker1.is_available.return_value = True
    worker1.is_available_if_needed.return_value = False

    worker2 = MagicMock(spec=Worker, name='Konrad')
    worker2.name = 'Konrad'
    worker2.position = 'Student'
    worker2.is_available.return_value = True
    worker2.is_available_if_needed.return_value = False

    worker3 = MagicMock(spec=Worker, name='Natalia')
    worker3.name = 'Natalia'
    worker3.position = 'Regular'
    worker3.is_available.return_value = True
    worker3.is_available_if_needed.return_value = False

    worker_manager = MagicMock(spec=Worker_Manager)
    worker_manager.position_priorities = {"CEO": 1, "Regular": 2, "Student": 3}
    worker_manager.get_days.return_value = ['21.07']
    worker_manager.get_sorted_workers_by_position_priority.return_value = [worker1, worker3, worker2]

    worker_manager.workers_list = [worker1, worker2, worker3]
    return worker_manager


@pytest.fixture
def scheduler_r_three_workers_needed_for_one_time_normal_availability_sorted_priority(
        mock_worker_manager_three_workers_normal_availability_sorted_priority):
    accuracy = 1
    allocation = {"7:00-8:00": 3}
    scheduler = Scheduler_r("R", accuracy=accuracy, allocation=allocation)
    scheduler.worker_manager = mock_worker_manager_three_workers_normal_availability_sorted_priority
    return scheduler


def test_make_schedule_three_workers_needed_for_one_time_normal_availability_sorted_priority(
        scheduler_r_three_workers_needed_for_one_time_normal_availability_sorted_priority):
    schedule = scheduler_r_three_workers_needed_for_one_time_normal_availability_sorted_priority.make_schedule()
    assert '21.07' in schedule
    assert len(schedule['21.07']['07:00-08:00']) == 3
    assert schedule['21.07']['07:00-08:00'][0].name == "Konrad"
    assert schedule['21.07']['07:00-08:00'][1].name == "Natalia"
    assert schedule['21.07']['07:00-08:00'][2].name == "Filip"


# Lower priority workers are assigned if higher are unavailable ________________
@pytest.fixture
def mock_worker_manager_three_workers_normal_availability_highest_unavailable_sorted_priority():
    worker1 = MagicMock(spec=Worker, name='Filip')
    worker1.name = 'Filip'
    worker1.position = 'CEO'
    worker1.is_available.return_value = True
    worker1.is_available_if_needed.return_value = False

    worker2 = MagicMock(spec=Worker, name='Konrad')
    worker2.name = 'Konrad'
    worker2.position = 'Student'
    worker2.is_available.return_value = False
    worker2.is_available_if_needed.return_value = False

    worker3 = MagicMock(spec=Worker, name='Natalia')
    worker3.name = 'Natalia'
    worker3.position = 'Regular'
    worker3.is_available.return_value = True
    worker3.is_available_if_needed.return_value = False

    worker_manager = MagicMock(spec=Worker_Manager)
    worker_manager.position_priorities = {"CEO": 1, "Regular": 2, "Student": 3}
    worker_manager.get_days.return_value = ['21.07']
    worker_manager.get_sorted_workers_by_position_priority.return_value = [worker1, worker3, worker2]

    worker_manager.workers_list = [worker1, worker2, worker3]

    return worker_manager


@pytest.fixture
def scheduler_r_three_workers_needed_for_one_time_normal_availability_highest_unavailable_sorted_priority(
        mock_worker_manager_three_workers_normal_availability_highest_unavailable_sorted_priority):
    accuracy = 1
    allocation = {"7:00-8:00": 3}
    scheduler = Scheduler_r("R", accuracy=accuracy, allocation=allocation)
    scheduler.worker_manager = mock_worker_manager_three_workers_normal_availability_highest_unavailable_sorted_priority
    return scheduler


def test_make_schedule_three_workers_needed_for_one_time_normal_availability_highest_unavailable_sorted_priority(
        scheduler_r_three_workers_needed_for_one_time_normal_availability_highest_unavailable_sorted_priority):
    schedule = scheduler_r_three_workers_needed_for_one_time_normal_availability_highest_unavailable_sorted_priority.make_schedule()
    assert '21.07' in schedule
    assert len(schedule['21.07']['07:00-08:00']) == 3
    assert schedule['21.07']['07:00-08:00'][0].name == "Natalia"
    assert schedule['21.07']['07:00-08:00'][1].name == "Filip"
    assert schedule['21.07']['07:00-08:00'][2] == "No worker available"


# Checking for previous and least used workers _____________________________________________________
# Previous time frame worker is re-utilized if available _______________________
@pytest.fixture
def scheduler_r_two_workers_normal_availability_previous_is_re_utilized(
        mock_worker_manager_two_workers_normal_availability):
    accuracy = 1
    allocation = {"7:00-8:00": 1, "8:00-9:00": 1}
    scheduler = Scheduler_r("R", accuracy=accuracy, allocation=allocation)
    scheduler.worker_manager = mock_worker_manager_two_workers_normal_availability
    return scheduler


def test_make_schedule_two_workers_normal_availability_previous_is_re_utilized(
        scheduler_r_two_workers_normal_availability_previous_is_re_utilized):
    schedule = scheduler_r_two_workers_normal_availability_previous_is_re_utilized.make_schedule()
    assert '21.07' in schedule
    assert len(schedule['21.07']['07:00-08:00']) == 1
    assert len(schedule['21.07']['08:00-09:00']) == 1
    assert schedule['21.07']['07:00-08:00'][0].name == "Konrad"
    assert schedule['21.07']['08:00-09:00'][0].name == "Konrad"


# Least used worker is prioritized if previous not available ___________________
@pytest.fixture
def mock_worker_manager_three_workers_one_least_used_worker():
    worker1 = MagicMock(spec=Worker, name='Filip')
    worker1.name = 'Filip'
    worker1.position = 'Student'
    worker1.is_available.side_effect = lambda day, time_frame: time_frame in ["11:00-12:00"]
    worker1.is_available_if_needed.return_value = False

    worker2 = MagicMock(spec=Worker, name='Konrad')
    worker2.name = 'Konrad'
    worker2.position = 'Student'
    worker2.is_available.side_effect = lambda day, time_frame: time_frame in ["07:00-08:00", "09:00-10:00",
                                                                              "11:00-12:00"]
    worker2.is_available_if_needed.return_value = False

    worker3 = MagicMock(spec=Worker, name='Natalia')
    worker3.name = 'Natalia'
    worker3.position = 'Student'
    worker3.is_available.side_effect = lambda day, time_frame: time_frame in ["08:00-09:00", "10:00-11:00"]
    worker3.is_available_if_needed.return_value = False

    worker_manager = MagicMock(spec=Worker_Manager)
    worker_manager.get_days.return_value = ['21.07']
    worker_manager.get_sorted_workers_by_position_priority.return_value = [worker1, worker2, worker3]

    worker_manager.workers_list = [worker1, worker2, worker3]

    return worker_manager


@pytest.fixture
def scheduler_r_three_workers_one_least_used_worker(
        mock_worker_manager_three_workers_one_least_used_worker):
    accuracy = 1
    allocation = {"7:00-12:00": 1}
    scheduler = Scheduler_r("R", accuracy=accuracy, allocation=allocation)
    scheduler.worker_manager = mock_worker_manager_three_workers_one_least_used_worker
    return scheduler


def test_make_schedule_scheduler_r_three_workers_one_least_used_worker(
        scheduler_r_three_workers_one_least_used_worker):
    schedule = scheduler_r_three_workers_one_least_used_worker.make_schedule()
    assert '21.07' in schedule
    assert len(schedule['21.07']['07:00-08:00']) == 1
    assert len(schedule['21.07']['08:00-09:00']) == 1
    assert len(schedule['21.07']['09:00-10:00']) == 1
    assert len(schedule['21.07']['10:00-11:00']) == 1
    assert len(schedule['21.07']['11:00-12:00']) == 1
    assert schedule['21.07']['07:00-08:00'][0].name == "Konrad"
    assert schedule['21.07']['08:00-09:00'][0].name == "Natalia"
    assert schedule['21.07']['09:00-10:00'][0].name == "Konrad"
    assert schedule['21.07']['10:00-11:00'][0].name == "Natalia"
    assert schedule['21.07']['11:00-12:00'][0].name == "Filip"

# New worker is added if neither previous nor least used is suitable ____________
@pytest.fixture
def mock_worker_manager_three_workers_no_previous_nor_least_used_worker():
    worker1 = MagicMock(spec=Worker, name='Filip')
    worker1.name = 'Filip'
    worker1.position = 'Student'
    worker1.is_available.side_effect = lambda day, time_frame: time_frame in ["07:00-08:00", "10:00-11:00",
                                                                              "11:00-12:00", "14:00-15:00"]
    worker1.is_available_if_needed.return_value = False

    worker2 = MagicMock(spec=Worker, name='Konrad')
    worker2.name = 'Konrad'
    worker2.position = 'Student'
    worker2.is_available.side_effect = lambda day, time_frame: time_frame in ["08:00-09:00"]    # Least used
    worker2.is_available_if_needed.return_value = False

    worker3 = MagicMock(spec=Worker, name='Natalia')
    worker3.name = 'Natalia'
    worker3.position = 'Student'
    worker3.is_available.side_effect = lambda day, time_frame: time_frame in ["09:00-10:00", "12:00-13:00",
                                                                              "13:00-14:00"]
    worker3.is_available_if_needed.return_value = False

    worker_manager = MagicMock(spec=Worker_Manager)
    worker_manager.get_days.return_value = ['21.07']
    worker_manager.get_sorted_workers_by_position_priority.return_value = [worker1, worker2, worker3]

    worker_manager.workers_list = [worker1, worker2, worker3]

    return worker_manager

@pytest.fixture
def scheduler_r_three_workers_no_previous_nor_least_used_worker(
        mock_worker_manager_three_workers_no_previous_nor_least_used_worker):
    accuracy = 1
    allocation = {"7:00-15:00": 1}
    scheduler = Scheduler_r("R", accuracy=accuracy, allocation=allocation)
    scheduler.worker_manager = mock_worker_manager_three_workers_no_previous_nor_least_used_worker
    return scheduler


def test_make_schedule_scheduler_r_no_previous_nor_least_used_worker(
        scheduler_r_three_workers_no_previous_nor_least_used_worker):
    schedule_instance = scheduler_r_three_workers_no_previous_nor_least_used_worker
    schedule = scheduler_r_three_workers_no_previous_nor_least_used_worker.make_schedule()

    mock_worker1, mock_worker2, mock_worker3 = schedule_instance.worker_manager.workers_list
    least_used_workers = schedule_instance._get_least_used_workers()

    assert '21.07' in schedule
    assert len(schedule['21.07']['07:00-08:00']) == 1
    assert len(schedule['21.07']['08:00-09:00']) == 1
    assert len(schedule['21.07']['09:00-10:00']) == 1
    assert len(schedule['21.07']['10:00-11:00']) == 1
    assert len(schedule['21.07']['11:00-12:00']) == 1
    assert schedule['21.07']['07:00-08:00'][0].name == "Filip"
    assert schedule['21.07']['08:00-09:00'][0].name == "Konrad"
    assert schedule['21.07']['09:00-10:00'][0].name == "Natalia"
    assert schedule['21.07']['10:00-11:00'][0].name == "Filip"
    assert schedule['21.07']['11:00-12:00'][0].name == "Filip"
    assert schedule['21.07']['12:00-13:00'][0].name == "Natalia"
    assert schedule['21.07']['13:00-14:00'][0].name == "Natalia"
    assert schedule['21.07']['14:00-15:00'][0].name == "Filip"
    assert mock_worker1 not in least_used_workers
    assert mock_worker2 in least_used_workers
    assert mock_worker3 not in least_used_workers
