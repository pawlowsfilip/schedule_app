import pytest
from scheduler_factory import SchedulerFactory
from scheduler.variants import scheduler_r, scheduler_s


def test_get_scheduler_returns_scheduler_r_for_variant_r():
    scheduler = SchedulerFactory.get_scheduler('R')
    assert isinstance(scheduler, scheduler_r.Scheduler_r)


def test_get_scheduler_returns_scheduler_s_for_variant_s():
    scheduler = SchedulerFactory.get_scheduler('S')
    assert isinstance(scheduler, scheduler_s.Scheduler_s)


def test_get_scheduler_returns_none_for_unsupported():
    scheduler = SchedulerFactory.get_scheduler(None)
    assert scheduler is None


def test_scheduler_r_with_parameters():
    accuracy = 1
    allocation = {"7:00-10:00": 1, "10:00-14:00": 2}
    variant = 'R'

    scheduler = SchedulerFactory.get_scheduler(variant=variant, accuracy=accuracy, allocation=allocation)

    assert scheduler.accuracy == accuracy
    assert scheduler.allocation == allocation
    assert scheduler.variant == variant


def test_scheduler_s_with_parameters():
    time_frames = {'21.07': [{"start": "8:00", "end": "8:15", "allocation": 1},
               {"start": "9:00", "end": "9:15", "allocation": 2}]}
    start = "7:00"
    end = "14:00"
    variant = 'S'

    scheduler = SchedulerFactory.get_scheduler(variant=variant, time_frames=time_frames, start=start, end=end)

    assert scheduler.time_frames == time_frames
    assert scheduler.start == start
    assert scheduler.end == end
    assert scheduler.variant == variant
