import pytest
from scheduler.variants.scheduler_s import Scheduler_s


@pytest.mark.parametrize("time_frame, expected_workers", [
    ("8:00-8:15", 1),
    ("8:05-8:10", 1),
    ("8:00-8:05", 1),
    ("9:00-9:15", 2),
    ("9:05-9:10", 2),
    ("9:00-9:05", 2),
    ("9:15-9:30", None),
    (None, None),
])
def test_get_needed_workers_for_time_frame_empty_time_frame(time_frame, expected_workers):
    scheduler = Scheduler_s("S", time_frames={"21.07": [{"start": "8:00", "end": "8:15", "allocation": 1},
                                                        {"start": "9:00", "end": "9:15", "allocation": 2}]},
                            start="8:00", end="9:15")
    assert scheduler.get_needed_workers_for_time_frame(time_frame) == expected_workers
