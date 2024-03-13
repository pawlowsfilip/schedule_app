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
    ├── Workers sorted by position priority
    │   ├── Highest priority workers are assigned first
    │   └── Lower priority workers are assigned if higher are unavailable
    └── Checking for previous and least used workers
        ├── Previous time frame worker is re-utilized if available
        ├── Least used worker is prioritized if previous not available
        └── New worker is added if neither previous nor least used is suitable
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
    assert '07:00-08:00' in schedule['21.07']
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
    assert '07:00-08:00' in schedule['21.07']
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
    assert '07:00-08:00' in schedule['21.07']
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
    assert '07:00-08:00' in schedule['21.07']
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
    assert '07:00-08:00' in schedule['21.07']
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
    assert '07:00-08:00' in schedule['21.07']
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
    assert '07:00-08:00' in schedule['21.07']
    assert len(schedule['21.07']['07:00-08:00']) == 2
    assert schedule['21.07']['07:00-08:00'][0].name == "Konrad"
    assert schedule['21.07']['07:00-08:00'][1] == "No worker available"


"""
TBD
"""