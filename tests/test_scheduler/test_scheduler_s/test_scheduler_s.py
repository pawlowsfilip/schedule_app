from scheduler.variants.scheduler_s import Scheduler_s
import pytest
from worker_manager import Worker_Manager
from worker import Worker
from unittest.mock import MagicMock

"""
make_schedule()
├── No Workers Needed for Any Time Frame - DONE
│   └── Schedule reflects empty list for all time frames - DONE
├── Workers Needed and Available
│   ├── All time frames have sufficient workers available
│   └── Specific time frames have no available workers, leading to "No worker available" entries
├── Previous Worker Utilization
│   ├── Previous worker is re-utilized for consecutive time frames when available
│   └── Previous worker not available leads to searching for other available workers
├── Least Used Worker Selection
│   ├── Least used worker is chosen to balance work distribution
│   └── All workers equally used does not prioritize any for least usage
├── Worker Availability Handling
│   ├── Normal availability fills the need before "worse" availability
│   └── "Worse" availability used only when normal availability insufficient
├── Fallback to "No Worker Available"
│   └── Time frames with insufficient workers list "No worker available"
├── Complex Scenario Handling
│   └── Mixed needs and availabilities across days and time frames are accurately scheduled
├── Edge Case and Invalid Input Handling
│   ├── Incorrect day formats or non-existent time frames result in appropriate handling or errors
│   └── Zero or excessive workers needed are handled correctly
└── Integration and Schedule Accuracy
    ├── Integration with Worker_Manager methods is correctly utilized
    └── Final schedule accurately represents worker assignments based on availability and needs

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
# @pytest.fixture
# def mock_worker_manager_two_workers_normal_availability():
#     worker1 = MagicMock(spec=Worker, name='Filip')
#     worker1.name = 'Filip'
#     worker1.position = 'Student'
#     worker1.is_available.side_effect = lambda day, time_frame: time_frame in ["08:00-08:15"]
#     worker1.is_available_if_needed.return_value = False
#
#     worker2 = MagicMock(spec=Worker, name='Konrad')
#     worker2.name = 'Konrad'
#     worker2.position = 'Student'
#     worker2.is_available.side_effect = lambda day, time_frame: time_frame in ["09:00-09:15"]
#     worker2.is_available_if_needed.return_value = False
#
#     worker_manager = MagicMock(spec=Worker_Manager)
#     worker_manager.get_days.return_value = ['21.07']
#     worker_manager.workers_list = [worker1, worker2]
#
#     return worker_manager
#
#
# @pytest.fixture
# def scheduler_r_two_workers_needed_for_two_time_frames_normal_availability(
#         mock_worker_manager_two_workers_normal_availability):
#     scheduler = Scheduler_s("S", time_frames={"21.07": [{"start": "8:00", "end": "8:15", "allocation": 1},
#                                                         {"start": "9:00", "end": "9:15", "allocation": 1}]})
#     scheduler.worker_manager = mock_worker_manager_two_workers_normal_availability
#     return scheduler
#
#
# def test_make_schedule_needed_for_two_time_frames_normal_availability(
#         scheduler_r_two_workers_needed_for_two_time_frames_normal_availability):
#     scheduler = scheduler_r_two_workers_needed_for_two_time_frames_normal_availability
#     schedule = scheduler.make_schedule()
#
#     # Validate that the schedule for '21.07' contains lists mapped by time frames
#     assert isinstance(schedule['21.07'], dict)
#     for workers in schedule['21.07'].values():
#         assert isinstance(workers, list)  # Each time frame should map to a list of workers

