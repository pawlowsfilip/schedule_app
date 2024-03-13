import pytest
from scheduler.variants.scheduler_r import Scheduler_r


@pytest.fixture
def scheduler_r_instance():
    accuracy = 1
    allocation = {"7:00-10:00": 1, "10:00-14:00": 2}
    return Scheduler_r("R", accuracy=accuracy, allocation=allocation)


def test_init_of_scheduler_r(scheduler_r_instance):
    assert scheduler_r_instance.variant == "R"
    assert scheduler_r_instance.accuracy == 1
    assert scheduler_r_instance.allocation == {"7:00-10:00": 1, "10:00-14:00": 2}
    assert isinstance(scheduler_r_instance.schedule, dict)
