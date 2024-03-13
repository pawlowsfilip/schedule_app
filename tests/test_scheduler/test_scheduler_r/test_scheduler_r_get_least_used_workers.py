import pytest
from scheduler.variants.scheduler_r import Scheduler_r


@pytest.fixture
def scheduler_r_instance():
    accuracy = 1
    allocation = {"7:00-10:00": 1, "10:00-14:00": 2}
    return Scheduler_r("R", accuracy=accuracy, allocation=allocation)


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