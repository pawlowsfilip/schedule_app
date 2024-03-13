from scheduler.variants.scheduler_r import Scheduler_r


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
