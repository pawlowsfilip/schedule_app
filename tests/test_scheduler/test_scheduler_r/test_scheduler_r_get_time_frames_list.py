from scheduler.variants.scheduler_r import Scheduler_r


def test_get_time_frames_list_no_allocation():
    scheduler = Scheduler_r("R", accuracy=1.0, allocation={})
    assert scheduler._get_time_frames_list() is None


def test_get_time_frames_list_one_hour_allocation_one_hour_accuracy_one_time_frames():
    scheduler = Scheduler_r("R", accuracy=1.0, allocation={"7:00-8:00": 2})
    assert scheduler._get_time_frames_list() == ["07:00-08:00"]


def test_get_time_frames_list_one_hour_allocation_half_hour_accuracy_multiple_time_frames():
    scheduler = Scheduler_r("R", accuracy=0.5, allocation={"7:00-8:00": 2})
    assert scheduler._get_time_frames_list() == ["07:00-07:30", "07:30-08:00"]


def test_get_time_frames_list_one_hour_allocation_quarter_hour_accuracy_multiple_time_frames():
    scheduler = Scheduler_r("R", accuracy=0.25, allocation={"7:00-8:00": 2})
    assert scheduler._get_time_frames_list() == ["07:00-07:15", "07:15-07:30", "07:30-07:45", "07:45-08:00"]


def test_get_time_frames_list_two_hours_allocation_one_hour_accuracy_multiple_time_frames():
    scheduler = Scheduler_r("R", accuracy=1.0, allocation={"7:00-9:00": 2})
    assert scheduler._get_time_frames_list() == ["07:00-08:00", "08:00-09:00"]


def test_get_time_frames_list_two_hours_allocation_half_hour_accuracy_multiple_time_frames():
    scheduler = Scheduler_r("R", accuracy=0.5, allocation={"7:00-9:00": 2})
    assert scheduler._get_time_frames_list() == ["07:00-07:30", "07:30-08:00", "08:00-08:30", "08:30-09:00"]
