import pytest
from scheduler.variants.scheduler_r import Scheduler_r


@pytest.mark.parametrize("time_frame, expected_workers", [
    ("9:00-13:00", 2),
    ("10:00-11:00", 2),
    ("9:00-12:00", 2),
    ("13:00-14:00", 3),
    ("15:00-16:00", None),
    ("13:00-15:00", 3),
    (None, None),
])
def test_get_needed_workers_for_time_frame_empty_time_frame(time_frame, expected_workers):
    scheduler = Scheduler_r("R", accuracy=1.0, allocation={"9:00-13:00": 2, "13:00-15:00": 3})
    assert scheduler.get_needed_workers_for_time_frame(time_frame) == expected_workers
