from datetime import datetime, time
from worker import Worker
import pytest


def test_init_with_all_arguments():
    worker = Worker(name='John Doe', availability={'21.07': '8:00-10:00'}, worse_availability={'21.07': '10:00-14:00'},
                    position='Manager')
    assert worker.get_name() == 'John Doe'
    assert worker.get_availability() == {'21.07': '8:00-10:00'}
    assert worker.get_worse_availability() == {'21.07': '10:00-14:00'}
    assert worker.get_position() == 'Manager'


def test_init_with_necessary_arguments():
    worker = Worker(name="John Doe", availability={'21.07': '8:00-10:00'})
    assert worker.get_name() == "John Doe"
    assert worker.get_availability() == {'21.07': '8:00-10:00'}
    assert worker.get_worse_availability() is None
    assert worker.get_position() is None

