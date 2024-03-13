from scheduler.variants.scheduler_r import Scheduler_r

def test_get_working_hours_no_allocation():
    scheduler = Scheduler_r("R", accuracy=1.0, allocation={})
    assert scheduler._get_working_hours() == (None, None)


def test_get_working_hours_one_allocation():
    scheduler = Scheduler_r("R", accuracy=1.0, allocation={"10:00-14:00": 2})
    assert scheduler._get_working_hours() == ("10:00", "14:00")


def test_get_working_hours_multiple_allocations():
    scheduler = Scheduler_r("R", accuracy=1.0, allocation={"7:00-9:00": 2, "9:00-12:00": 2, "12:00-18:00": 3})
    assert scheduler._get_working_hours() == ("07:00", "18:00")
