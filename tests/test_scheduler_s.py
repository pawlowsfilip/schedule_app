from datetime import datetime, time
from scheduler.scheduler import Scheduler
from scheduler.variants.scheduler_s import Scheduler_s
import pytest


def test_init_with_all_arguments():
    scheduler = Scheduler_s({'21.07': [{"start": "8:00", "end": "8:15", "allocation": 1},
                                       {"start": "9:00", "end": "9:15", "allocation": 2}]}, "S", "7:00", "14:00")
    assert scheduler.time_frames == {'21.07': [{"start": "8:00", "end": "8:15", "allocation": 1},
                                               {"start": "9:00", "end": "9:15", "allocation": 2}]}
    assert scheduler.variant == "S"


def test_get_time_frames_list_for_one_time_frame():
    scheduler = Scheduler_s({'21.07': [{"start": "8:00", "end": "8:15", "allocation": 1}]}, "S", "7:00", "14:00")
    assert len(scheduler._get_time_frames_list()) == 1


def test_get_time_frames_list_for_more_than_one_time_frame():
    scheduler = Scheduler_s({'21.07': [{"start": "8:00", "end": "8:15", "allocation": 1},
                                       {"start": "9:00", "end": "9:15", "allocation": 2}]}, "S", "7:00", "14:00")
    assert len(scheduler._get_time_frames_list()) == 2

