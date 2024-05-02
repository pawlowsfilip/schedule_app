# import pytest
# from scheduler.variants.scheduler_s import Scheduler_s
# from unittest.mock import patch, MagicMock
# from worker import Worker
# from worker_manager import Worker_Manager
#
# """
# _get_least_used_workers()
# ├── No workers are assigned to any time frames - DONE
# ├── One worker is least used among others - DONE
# ├── Workers have equal usage across time frames - DONE
# └── Workers have different usage across multiple days - DONE
# """
#
#
# # No workers are assigned to any time frames _______________________________________________________
# @pytest.fixture
# def scheduler_s_no_workers():
#     scheduler = Scheduler_s("S", time_frames={"21.07": [{"start": "8:00", "end": "8:15", "allocation": 1},
#                                                         {"start": "9:00", "end": "9:15", "allocation": 2}]})
#     return scheduler
#
#
# def test_get_least_used_workers_no_workers(scheduler_s_no_workers):
#     assert scheduler_s_no_workers._get_least_used_workers() == []
#
#
# # One worker is least used among others ____________________________________________________________
# @pytest.fixture
# def mock_worker_manager_three_workers_one_least_used():
#     worker1 = MagicMock(spec=Worker, name='Filip')
#     worker1.name = 'Filip'
#     worker1.position = 'Student'
#
#     worker2 = MagicMock(spec=Worker, name='Konrad')
#     worker2.name = 'Konrad'
#     worker2.position = 'Student'
#
#     worker3 = MagicMock(spec=Worker, name='Ola')
#     worker3.name = 'Ola'
#     worker3.position = 'Student'
#
#     worker_manager = MagicMock(spec=Worker_Manager)
#     worker_manager.get_days.return_value = ['21.07']
#     worker_manager.get_sorted_workers_by_position_priority.return_value = [worker1, worker2, worker3]
#     worker_manager.workers_list = [worker1, worker2, worker3]
#
#     return worker_manager
#
#
# @pytest.fixture
# def scheduler_r_instance_three_workers_one_least_used(mock_worker_manager_three_workers_one_least_used):
#     scheduler = Scheduler_s("S", time_frames={"21.07": [{"start": "8:00", "end": "8:15", "allocation": 2},
#                                                         {"start": "9:00", "end": "9:15", "allocation": 2},
#                                                         {"start": "10:00", "end": "10:15", "allocation": 2},
#                                                         {"start": "11:00", "end": "11:15", "allocation": 2}]})
#     scheduler.worker_manager = mock_worker_manager_three_workers_one_least_used
#     scheduler.schedule = {
#         "21.07": {
#             "8:00-8:15": [scheduler.worker_manager.workers_list[0], scheduler.worker_manager.workers_list[1]],
#             "9:00-9:15": [scheduler.worker_manager.workers_list[1], scheduler.worker_manager.workers_list[2]],
#             "10:00-10:15": [scheduler.worker_manager.workers_list[0], scheduler.worker_manager.workers_list[2]],
#             "11:00-11:15": [scheduler.worker_manager.workers_list[0], scheduler.worker_manager.workers_list[1]]
#         }
#     }
#     return scheduler
#
#
# def test_get_least_used_workers_one_worker(scheduler_r_instance_three_workers_one_least_used):
#     scheduler = scheduler_r_instance_three_workers_one_least_used
#     mock_worker1, mock_worker2, mock_worker3 = scheduler.worker_manager.workers_list
#     least_use_workers = scheduler._get_least_used_workers()
#
#     assert mock_worker1 not in least_use_workers
#     assert mock_worker2 not in least_use_workers
#     assert mock_worker3 in least_use_workers
#     assert len(least_use_workers) == 1
#
#
# # Workers have equal usage across time frames ______________________________________________________
# @pytest.fixture
# def mock_worker_manager_equal_usage():
#     worker1 = MagicMock(spec=Worker, name='Filip')
#     worker1.name = 'Filip'
#     worker1.position = 'Student'
#
#     worker2 = MagicMock(spec=Worker, name='Konrad')
#     worker2.name = 'Konrad'
#     worker2.position = 'Student'
#
#     worker3 = MagicMock(spec=Worker, name='Ola')
#     worker3.name = 'Ola'
#     worker3.position = 'Student'
#
#     worker_manager = MagicMock(spec=Worker_Manager)
#     worker_manager.get_days.return_value = ['21.07']
#     worker_manager.get_sorted_workers_by_position_priority.return_value = [worker1, worker2, worker3]
#     worker_manager.workers_list = [worker1, worker2, worker3]
#
#     return worker_manager
#
#
# @pytest.fixture
# def scheduler_r_instance_equal_usage(mock_worker_manager_equal_usage):
#     scheduler = Scheduler_s("S", time_frames={"21.07": [{"start": "8:00", "end": "8:15", "allocation": 2},
#                                                         {"start": "9:00", "end": "9:15", "allocation": 2},
#                                                         {"start": "10:00", "end": "10:15", "allocation": 2}]})
#     scheduler.worker_manager = mock_worker_manager_equal_usage
#     scheduler.schedule = {
#         "21.07": {
#             "8:00-8:15": [scheduler.worker_manager.workers_list[0], scheduler.worker_manager.workers_list[1]],
#             "9:00-9:15": [scheduler.worker_manager.workers_list[1], scheduler.worker_manager.workers_list[2]],
#             "10:00-10:15": [scheduler.worker_manager.workers_list[0], scheduler.worker_manager.workers_list[2]],
#         }
#     }
#     return scheduler
#
#
# def test_get_least_used_workers_equal_usage(scheduler_r_instance_equal_usage):
#     scheduler = scheduler_r_instance_equal_usage
#     mock_worker1, mock_worker2, mock_worker3 = scheduler.worker_manager.workers_list
#     least_use_workers = scheduler._get_least_used_workers()
#
#     assert mock_worker1 not in least_use_workers
#     assert mock_worker2 not in least_use_workers
#     assert mock_worker3 not in least_use_workers
#     assert len(least_use_workers) == 0
#
#
# # Workers have different usage across multiple days ________________________________________________
# @pytest.fixture
# def mock_worker_manager_two_workers_least_used_different_days():
#     worker1 = MagicMock(spec=Worker, name='Filip')
#     worker1.name = 'Filip'
#     worker1.position = 'Student'
#
#     worker2 = MagicMock(spec=Worker, name='Konrad')
#     worker2.name = 'Konrad'
#     worker2.position = 'Student'
#
#     worker3 = MagicMock(spec=Worker, name='Ola')
#     worker3.name = 'Ola'
#     worker3.position = 'Student'
#
#     worker4 = MagicMock(spec=Worker, name='Natalia')
#     worker4.name = 'Natalia'
#     worker4.position = 'Student'
#
#     worker_manager = MagicMock(spec=Worker_Manager)
#     worker_manager.get_days.return_value = ['21.07', '22.07']
#     worker_manager.get_sorted_workers_by_position_priority.return_value = [worker1, worker2, worker3, worker4]
#     worker_manager.workers_list = [worker1, worker2, worker3, worker4]
#
#     return worker_manager
#
#
# @pytest.fixture
# def scheduler_r_instance_two_workers_least_used_different_days(
#         mock_worker_manager_two_workers_least_used_different_days):
#     scheduler = Scheduler_s("S", time_frames={"21.07": [{"start": "8:00", "end": "8:15", "allocation": 2},
#                                                         {"start": "9:00", "end": "9:15", "allocation": 2},
#                                                         {"start": "10:00", "end": "10:15", "allocation": 2},
#                                                         {"start": "11:00", "end": "11:15", "allocation": 2}],
#                                               "22.07": [{"start": "8:00", "end": "8:15", "allocation": 2},
#                                                         {"start": "9:00", "end": "9:15", "allocation": 2},
#                                                         {"start": "10:00", "end": "10:15", "allocation": 2},
#                                                         {"start": "11:00", "end": "11:15", "allocation": 2}]
#                                               })
#     scheduler.worker_manager = mock_worker_manager_two_workers_least_used_different_days
#     scheduler.schedule = {
#         "21.07": {
#             "8:00-8:15": [scheduler.worker_manager.workers_list[0], scheduler.worker_manager.workers_list[1]],
#             "9:00-9:15": [scheduler.worker_manager.workers_list[1], scheduler.worker_manager.workers_list[2]],
#             "10:00-10:15": [scheduler.worker_manager.workers_list[0], scheduler.worker_manager.workers_list[2]],
#             "11:00-11:15": [scheduler.worker_manager.workers_list[0], scheduler.worker_manager.workers_list[1]]
#         },
#         "22.07": {
#             "8:00-8:15": [scheduler.worker_manager.workers_list[0], scheduler.worker_manager.workers_list[1]],
#             "9:00-9:15": [scheduler.worker_manager.workers_list[1], scheduler.worker_manager.workers_list[3]],
#             "10:00-10:15": [scheduler.worker_manager.workers_list[0], scheduler.worker_manager.workers_list[3]],
#             "11:00-11:15": [scheduler.worker_manager.workers_list[0], scheduler.worker_manager.workers_list[1]]
#         }
#     }
#     return scheduler
#
#
# def test_get_least_used_workers_two_workers_least_used_different_days(
#         scheduler_r_instance_two_workers_least_used_different_days):
#     scheduler = scheduler_r_instance_two_workers_least_used_different_days
#     mock_worker1, mock_worker2, mock_worker3, mock_worker4 = scheduler.worker_manager.workers_list
#     least_use_workers = scheduler._get_least_used_workers()
#
#     assert mock_worker1 not in least_use_workers
#     assert mock_worker2 not in least_use_workers
#
#     assert mock_worker3 in least_use_workers
#     assert mock_worker4 in least_use_workers
#     assert len(least_use_workers) == 2
