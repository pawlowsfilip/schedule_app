from scheduler.variants.scheduler_s import Scheduler_s
import pytest
from worker_manager import Worker_Manager
from worker import Worker
from unittest.mock import MagicMock

"""
make_schedule()
├── No Workers Needed for Any Time Frame - DONE
│   └── Schedule reflects "No worker needed" for all time frames - DONE
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

# @pytest.fixture
# def mock_worker_manager_no_workers_needed():
#     worker1 = MagicMock(spec=Worker, name='Filip')
#     worker1.name = 'Filip'
#     worker1.position = 'Student'
#
#     worker2 = MagicMock(spec=Worker, name='Konrad')
#     worker2.name = 'Konrad'
#     worker2.position = 'Student'
#
#     worker_manager = MagicMock(spec=Worker_Manager)
#     worker_manager.get_days.return_value = ['21.07']
#     worker_manager.get_sorted_workers_by_position_priority.return_value = [worker1, worker2]
#     worker_manager.workers_list = [worker1, worker2]
#
#     return worker_manager
#
# @pytest.fixture
# def scheduler_s_no_workers_needed(mock_worker_manager_no_workers_needed):
#     scheduler = Scheduler_s("S", time_frames={"21.07": [{"start": "8:00", "end": "8:15", "allocation": 0},
#                                                         {"start": "9:00", "end": "9:15", "allocation": 0}]})
#     worker_manager = mock_worker_manager_no_workers_needed
#     assert worker_manager.get_days() == ['21.07']
#     return scheduler
#
# def test_make_schedule_no_workers_needed(scheduler_s_no_workers_needed):
#     scheduler = scheduler_s_no_workers_needed
#     schedule = scheduler.make_schedule()


