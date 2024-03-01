from datetime import datetime, time
from scheduler.scheduler import Scheduler
from scheduler.variants.scheduler_s import Scheduler_s
import pytest


def test_init_with_all_arguments():
    scheduler = Scheduler_s({'21.07': ["start"]})