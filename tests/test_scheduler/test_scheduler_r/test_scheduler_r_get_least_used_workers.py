# import pytest
# from scheduler.variants.scheduler_r import Scheduler_r
# from unittest.mock import patch, MagicMock
# from worker import Worker
# from worker_manager import Worker_Manager
#
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
#
#     worker_manager.workers_list = [worker1, worker2, worker3]
#
#     return worker_manager
#
# @pytest.fixture
# def scheduler_r_instance():
#     accuracy = 1
#     allocation = {"7:00-10:00": 1, "10:00-14:00": 2}
#     return Scheduler_r("R", accuracy=accuracy, allocation=allocation)
#
#
# def test_get_least_used_workers_no_workers(scheduler_r_instance):
#     assert scheduler_r_instance._get_least_used_workers() == []
#
#
# @pytest.fixture
# def scheduler_r_instance_three_workers_one_least_used(mock_worker_manager_three_workers_one_least_used):
#     accuracy = 1
#     allocation = {"7:00-10:00": 1, "10:00-14:00": 2}
#     scheduler = Scheduler_r("R", accuracy=accuracy, allocation=allocation)
#     scheduler.worker_manager = mock_worker_manager_three_workers_one_least_used
#     return scheduler
#
# def test_get_least_used_workers_one_worker(scheduler_r_instance_three_workers_one_least_used):
#     scheduler_r_instance_three_workers_one_least_used.schedule = {"21.07": {
#         "7:00-8:00": ["Filip"], "8:00-9:00": ["Filip"], "9:00-10:00": ["Filip"],
#         "10:00-11:00": ["Konrad"], "11:00-12:00": ["Konrad"], "12:00-13:00": ["Konrad"], "13:00-14:00": ["Ola"]}}
#     least_use_workers = scheduler_r_instance_three_workers_one_least_used._get_least_used_workers()
#     assert "Ola" in least_use_workers and "Konrad" not in least_use_workers and "Filip" not in least_use_workers
#     assert len(least_use_workers) == 1
#
#
# def test_get_least_used_workers_equal_usage(scheduler_r_instance):
#     scheduler_r_instance.schedule = {"21.07": {"7:00-8:00": ["Filip"], "8:00-9:00": ["Filip"], "9:00-10:00": ["Filip"],
#                                                "10:00-11:00": ["Konrad"], "11:00-12:00": ["Konrad"],
#                                                "12:00-13:00": ["Konrad"]}}
#     least_use_workers = scheduler_r_instance._get_least_used_workers()
#     assert "Konrad" not in least_use_workers and "Filip" not in least_use_workers
#     assert len(least_use_workers) == 0
#
#
# def test_get_least_used_workers_two_workers_different_days(scheduler_r_instance):
#     scheduler_r_instance.schedule = {"21.07": {"7:00-8:00": ["Filip"], "8:00-9:00": ["Filip"], "9:00-10:00": ["Filip"],
#                                                "10:00-11:00": ["Konrad"], "11:00-12:00": ["Konrad"],
#                                                "12:00-13:00": ["Konrad"], "13:00-14:00": ["Ola"]},
#                                      "22.07": {"7:00-8:00": ["Filip"], "8:00-9:00": ["Filip"], "9:00-10:00": ["Filip"],
#                                                "10:00-11:00": ["Konrad"], "11:00-12:00": ["Konrad"],
#                                                "12:00-13:00": ["Konrad"], "13:00-14:00": ["Natalia"]}}
#     least_use_workers = scheduler_r_instance._get_least_used_workers()
#     assert "Ola" in least_use_workers and "Natalia" in least_use_workers and "Konrad" not in least_use_workers \
#            and "Filip" not in least_use_workers
#     assert len(least_use_workers) == 2
