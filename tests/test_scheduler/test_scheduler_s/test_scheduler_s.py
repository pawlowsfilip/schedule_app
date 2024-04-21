from scheduler.variants.scheduler_s import Scheduler_s
import pytest
from worker_manager import Worker_Manager
from worker import Worker
from unittest.mock import MagicMock

"""
make_schedule()
├── No Workers Needed for Any Time Frame - DONE
│   └── Schedule reflects empty list for all time frames - DONE
├── Workers Needed and Available - DONE
│   ├── All time frames have sufficient workers available - DONE
│   └── Specific time frames have no available workers, leading to "No worker available" entries - DONE
├── Previous Worker Utilization
│   ├── Previous worker is re-utilized for consecutive time frames when available - DONE
│   └── Previous worker not available leads to searching for other available workers - DONE
├── Least Used Worker Selection
│   ├── Least used worker is chosen to balance work distribution - DONE
│   └── All workers equally used does not prioritize any for least usage 
├── Worker Availability Handling
│   ├── Normal availability fills the need before "worse" availability
│   └── "Worse" availability used only when normal availability insufficient
├── Fallback to "No Worker Available"
│   └── Time frames with insufficient workers list "No worker available"
├── Complex Scenario Handling
│   └── Mixed needs and availabilities across days and time frames are accurately scheduled
├── Edge Case and Invalid Input Handling
    ├── Incorrect day formats or non-existent time frames result in appropriate handling or errors
    └── Zero or excessive workers needed are handled correctly


"""


# No Workers Needed for Any Time Frame _________________________________________________________________________________
# Schedule reflects empty list for all time frames _________________________________________________
@pytest.fixture
def scheduler_s_no_workers_needed():
    scheduler = Scheduler_s("S", time_frames={"21.07": [{"start": "8:00", "end": "8:15", "allocation": 0},
                                                        {"start": "9:00", "end": "9:15", "allocation": 0}]})
    scheduler.worker_manager = MagicMock()
    scheduler.worker_manager.get_days.return_value = ['21.07']

    return scheduler


def test_make_schedule_no_workers_needed(scheduler_s_no_workers_needed):
    scheduler = scheduler_s_no_workers_needed.make_schedule()
    assert scheduler['21.07'] == {}


# Workers Needed and Available__________________________________________________________________________________________
# All time frames have sufficient workers available ________________________________________________
@pytest.fixture
def mock_worker_manager_two_workers_normal_availability():
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
    worker_manager.workers_list = [worker1, worker2]

    def available_workers_mock(day, time_frame):
        if time_frame == "8:00-8:15":
            return [worker1]
        elif time_frame == "9:00-9:15":
            return [worker2]
        return []

    worker_manager.get_available_workers = MagicMock(side_effect=available_workers_mock)

    return worker_manager


@pytest.fixture
def scheduler_r_two_workers_needed_for_two_time_frames_normal_availability(
        mock_worker_manager_two_workers_normal_availability):
    scheduler = Scheduler_s("S", time_frames={"21.07": [{"start": "8:00", "end": "8:15", "allocation": 1},
                                                        {"start": "9:00", "end": "9:15", "allocation": 1}]})
    scheduler.worker_manager = mock_worker_manager_two_workers_normal_availability
    return scheduler


def test_make_schedule_needed_for_two_time_frames_normal_availability(
        scheduler_r_two_workers_needed_for_two_time_frames_normal_availability):
    scheduler = scheduler_r_two_workers_needed_for_two_time_frames_normal_availability
    schedule = scheduler.make_schedule()

    assert '21.07' in schedule
    assert schedule['21.07']['8:00-8:15'] == [scheduler.worker_manager.workers_list[0]]
    assert schedule['21.07']['9:00-9:15'] == [scheduler.worker_manager.workers_list[1]]


# Specific time frames have no available workers, leading to "No worker available" entries _________
@pytest.fixture
def mock_worker_manager_two_workers_no_availability():
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
    worker_manager.workers_list = [worker1, worker2]

    def available_workers_mock(day, time_frame):
        if time_frame == "8:00-8:15":
            pass
        elif time_frame == "9:00-9:15":
            pass
        return []

    worker_manager.get_available_workers = MagicMock(side_effect=available_workers_mock)

    return worker_manager


@pytest.fixture
def scheduler_r_two_workers_needed_for_two_time_frames_no_availability(
        mock_worker_manager_two_workers_no_availability):
    scheduler = Scheduler_s("S", time_frames={"21.07": [{"start": "8:00", "end": "8:15", "allocation": 1},
                                                        {"start": "9:00", "end": "9:15", "allocation": 1}]})
    scheduler.worker_manager = mock_worker_manager_two_workers_no_availability
    return scheduler


def test_make_schedule_needed_for_two_time_frames_no_availability(
        scheduler_r_two_workers_needed_for_two_time_frames_no_availability):
    scheduler = scheduler_r_two_workers_needed_for_two_time_frames_no_availability
    schedule = scheduler.make_schedule()

    assert '21.07' in schedule
    assert schedule['21.07']['8:00-8:15'] == ['No worker available']
    assert schedule['21.07']['9:00-9:15'] == ['No worker available']


# Previous Worker Utilization __________________________________________________________________________________________
# Previous worker is re-utilized for consecutive time frames when available ________________________
@pytest.fixture
def mock_worker_manager_two_workers_previous_re_utilized():
    worker1 = MagicMock(spec=Worker, name='Filip')
    worker1.name = 'Filip'
    worker1.position = 'Student'
    worker1.is_available.side_effect = lambda day, time_frame: time_frame in ["08:00-08:15", "09:00-09:15"]
    worker1.is_available_if_needed.return_value = False

    worker2 = MagicMock(spec=Worker, name='Konrad')
    worker2.name = 'Konrad'
    worker2.position = 'Student'
    worker2.is_available.side_effect = lambda day, time_frame: time_frame in ["09:00-09:15"]
    worker2.is_available_if_needed.return_value = False

    worker_manager = MagicMock(spec=Worker_Manager)
    worker_manager.get_days.return_value = ['21.07']
    worker_manager.workers_list = [worker1, worker2]

    def available_workers_mock(day, time_frame):
        if time_frame == "8:00-8:15":
            return [worker_manager.workers_list[0]]
        elif time_frame == "9:00-9:15":
            return [worker_manager.workers_list[0], worker_manager.workers_list[1]]
        return []

    worker_manager.get_available_workers = MagicMock(side_effect=available_workers_mock)

    return worker_manager


@pytest.fixture
def scheduler_r_two_workers_needed_for_two_time_frames_re_utilized(
        mock_worker_manager_two_workers_previous_re_utilized):
    scheduler = Scheduler_s("S", time_frames={"21.07": [{"start": "8:00", "end": "8:15", "allocation": 1},
                                                        {"start": "9:00", "end": "9:15", "allocation": 1}]})
    scheduler.worker_manager = mock_worker_manager_two_workers_previous_re_utilized
    return scheduler


def test_make_schedule_needed_for_two_time_frames_re_utilized(
        scheduler_r_two_workers_needed_for_two_time_frames_re_utilized):
    scheduler = scheduler_r_two_workers_needed_for_two_time_frames_re_utilized
    schedule = scheduler.make_schedule()

    assert '21.07' in schedule
    assert schedule['21.07']['8:00-8:15'] == [scheduler.worker_manager.workers_list[0]]
    assert schedule['21.07']['9:00-9:15'] == [scheduler.worker_manager.workers_list[0]]


# Previous worker not available leads to searching for other available workers _____________________
@pytest.fixture
def mock_worker_manager_two_workers_previous_not_re_utilized():
    worker1 = MagicMock(spec=Worker, name='Filip')
    worker1.name = 'Filip'
    worker1.position = 'Student'
    worker1.is_available.side_effect = lambda day, time_frame: time_frame in ["08:00-08:15", "09:00-09:15"]
    worker1.is_available_if_needed.return_value = False

    worker2 = MagicMock(spec=Worker, name='Konrad')
    worker2.name = 'Konrad'
    worker2.position = 'Student'
    worker2.is_available.side_effect = lambda day, time_frame: time_frame in ["09:00-09:15"]
    worker2.is_available_if_needed.return_value = False

    worker_manager = MagicMock(spec=Worker_Manager)
    worker_manager.get_days.return_value = ['21.07']
    worker_manager.workers_list = [worker1, worker2]

    def available_workers_mock(day, time_frame):
        if time_frame == "8:00-8:15":
            return [worker_manager.workers_list[0]]
        elif time_frame == "9:00-9:15":
            return [worker_manager.workers_list[1]]
        return []

    worker_manager.get_available_workers = MagicMock(side_effect=available_workers_mock)

    return worker_manager


@pytest.fixture
def scheduler_r_two_workers_needed_for_two_time_frames_not_re_utilized(
        mock_worker_manager_two_workers_previous_not_re_utilized):
    scheduler = Scheduler_s("S", time_frames={"21.07": [{"start": "8:00", "end": "8:15", "allocation": 1},
                                                        {"start": "9:00", "end": "9:15", "allocation": 1}]})
    scheduler.worker_manager = mock_worker_manager_two_workers_previous_not_re_utilized
    return scheduler


def test_make_schedule_needed_for_two_time_frames_not_re_utilized(
        scheduler_r_two_workers_needed_for_two_time_frames_not_re_utilized):
    scheduler = scheduler_r_two_workers_needed_for_two_time_frames_not_re_utilized
    schedule = scheduler.make_schedule()

    assert '21.07' in schedule
    assert schedule['21.07']['8:00-8:15'] == [scheduler.worker_manager.workers_list[0]]
    assert schedule['21.07']['9:00-9:15'] == [scheduler.worker_manager.workers_list[1]]


# Least Used Worker Selection __________________________________________________________________________________________
# Least used worker is chosen to balance work distribution _________________________________________
# @pytest.fixture
# def mock_worker_manager_three_workers_least_used_worker():
#     worker1 = MagicMock(spec=Worker, name='Filip')
#     worker1.name = 'Filip'
#     worker1.position = 'Student'
#     worker1.is_available.side_effect = lambda day, time_frame: time_frame in ["08:00-08:15", "09:00-09:15",
#                                                                               "12:00-12:15"]
#     worker1.is_available_if_needed.return_value = False
#
#     worker2 = MagicMock(spec=Worker, name='Konrad')
#     worker2.name = 'Konrad'
#     worker2.position = 'Student'
#     worker2.is_available.side_effect = lambda day, time_frame: time_frame in ["10:00-10:15", "11:00-11:15"]
#     worker2.is_available_if_needed.return_value = False
#
#     worker3 = MagicMock(spec=Worker, name='Ola')
#     worker3.name = 'Ola'
#     worker3.position = 'Student'
#     worker3.is_available.side_effect = lambda day, time_frame: time_frame in ["12:00-12:15"]
#     worker3.is_available_if_needed.return_value = False
#
#     worker_manager = MagicMock(spec=Worker_Manager)
#     worker_manager.get_days.return_value = ['21.07']
#     worker_manager.workers_list = [worker1, worker2, worker3]
#
#     worker_manager.get_available_workers = MagicMock(side_effect=lambda day, time_frame: [
#         worker for worker in [worker1, worker2, worker3] if worker.is_available(day, time_frame)
#     ])
#
#     return worker_manager, worker1, worker2, worker3
#
#
# @pytest.mark.parametrize(
#     "available_workers,expected_schedule",
#     [
#         (
#                 {'8:00-8:15': ['worker1'], '9:00-9:15': ['worker1'], '10:00-10:15': ['worker2'],
#                  '11:00-11:15': ['worker2'], '12:00-12:15': ['worker1', 'worker3']},
#                 {'21.07': {'8:00-8:15': ['worker1'], '9:00-9:15': ['worker1'], '10:00-10:15': ['worker2'],
#                            '11:00-11:15': ['worker2'], '12:00-12:15': ['worker3']}}
#         )
#     ]
# )
# def test_make_schedule_needed_for_five_time_frames_least_used(available_workers, expected_schedule,
#                                                               mock_worker_manager_three_workers_least_used_worker):
#     scheduler = Scheduler_s("S", time_frames={"21.07": [{"start": "8:00", "end": "8:15", "allocation": 1},
#                                                         {"start": "9:00", "end": "9:15", "allocation": 1},
#                                                         {"start": "10:00", "end": "10:15", "allocation": 1},
#                                                         {"start": "11:00", "end": "11:15", "allocation": 1},
#                                                         {"start": "12:00", "end": "12:15", "allocation": 1}]})
#     scheduler.worker_manager, scheduler.worker1, scheduler.worker2, scheduler.worker3 = mock_worker_manager_three_workers_least_used_worker
#     workers = {'worker1': scheduler.worker1, 'worker2': scheduler.worker2, 'worker3': scheduler.worker3}
#
#     # Adjust worker names to actual worker objects
#     for time_frame, worker_names in available_workers.items():
#         available_workers[time_frame] = [workers[worker_name] for worker_name in worker_names]
#
#     # scheduler.worker_manager = mock_worker_manager_three_workers_least_used_worker
#     scheduler.worker_manager.get_available_workers = MagicMock(
#         side_effect=lambda day, time_frame: available_workers.get(time_frame, []))
#
#     actual_schedule = scheduler.make_schedule()
#
#     assert actual_schedule == expected_schedule
