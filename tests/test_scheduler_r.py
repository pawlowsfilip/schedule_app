import pytest
from scheduler.variants.scheduler_r import Scheduler_r


@pytest.fixture()
def scheduler_r_instance():
    accuracy = 1
    allocation = {"7:00-10:00": 1, "10:00-14:00": 2}
    return Scheduler_r("R", accuracy=accuracy, allocation=allocation)


def test_init_of_scheduler_r(scheduler_r_instance):
    assert scheduler_r_instance.variant == "R"
    assert scheduler_r_instance.accuracy == 1
    assert scheduler_r_instance.allocation == {"7:00-10:00": 1, "10:00-14:00": 2}
    assert isinstance(scheduler_r_instance.schedule, dict)


# _get_working_hours _________________________________
def test_get_working_hours_no_allocation():
    scheduler = Scheduler_r("R", accuracy=1.0, allocation={})
    assert scheduler._get_working_hours() == (None, None)


def test_get_working_hours_one_allocation():
    scheduler = Scheduler_r("R", accuracy=1.0, allocation={"10:00-14:00": 2})
    assert scheduler._get_working_hours() == ("10:00", "14:00")


def test_get_working_hours_multiple_allocations():
    scheduler = Scheduler_r("R", accuracy=1.0, allocation={"7:00-9:00": 2, "9:00-12:00": 2, "12:00-18:00": 3})
    assert scheduler._get_working_hours() == ("07:00", "18:00")


# _number_of_time_frames_per_day _____________________
def test_number_of_time_frames_per_day_no_time_frames():
    scheduler = Scheduler_r("R", accuracy=1.0, allocation={})
    assert scheduler._number_of_time_frames_per_day() is None


def test_number_of_time_frames_per_day_one_time_frame_one_hour_accuracy():
    scheduler = Scheduler_r("R", accuracy=1.0, allocation={"7:00-8:00": 2})
    assert scheduler._number_of_time_frames_per_day() == 1


def test_number_of_time_frames_per_day_one_time_frame_half_hour_accuracy():
    scheduler = Scheduler_r("R", accuracy=0.5, allocation={"7:00-8:00": 2})
    assert scheduler._number_of_time_frames_per_day() == 2


def test_number_of_time_frames_per_day_one_time_frame_quarter_hour_accuracy():
    scheduler = Scheduler_r("R", accuracy=0.25, allocation={"7:00-8:00": 2})
    assert scheduler._number_of_time_frames_per_day() == 4


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


"""
TBD
"""