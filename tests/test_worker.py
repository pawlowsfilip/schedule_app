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
    worker = Worker(name='John Doe', availability={'21.07': '8:00-10:00'})
    assert worker.get_name() == 'John Doe'
    assert worker.get_availability() == {'21.07': '8:00-10:00'}
    assert worker.get_worse_availability() is None
    assert worker.get_position() is None


def test_worker_is_available_during_exact_time_frame():
    worker = Worker(name='John Doe', availability={'21.07': '8:00-10:00'})
    assert worker.is_available('21.07', '8:00-10:00') is True


def test_worker_is_available_during_time_frame():
    worker = Worker(name='John Doe', availability={'21.07': '8:00-10:00'})
    assert worker.is_available('21.07', '8:00-9:30') is True


def test_worker_is_not_available_during_exact_time_frame():
    worker = Worker(name='John Doe', availability={'21.07': '8:00-10:00'})
    assert worker.is_available('21.07', '12:00-13:00') is False


def test_worker_is_not_available_during_that_day():
    worker = Worker(name='John Doe', availability={'22.07': '8:00-10:00'})
    assert worker.is_available('21.07', '12:00-13:00') is False


def test_worker_is_available_but_overlap_time_frame():
    worker = Worker(name='John Doe', availability={'21.07': '8:00-10:00'})
    assert worker.is_available('21.07', '9:30-11:00') is True


def test_worker_is_available_if_needed_during_exact_time_frame():
    worker = Worker(name='John Doe', availability={'21.07': '8:00-10:00'}, worse_availability={'21.07': '10:00-14:00'})
    assert worker.is_available_if_needed('21.07', '10:00-14:00') is True


def test_worker_is_available_if_needed_during_time_frame():
    worker = Worker(name='John Doe', availability={'21.07': '8:00-10:00'}, worse_availability={'21.07': '10:00-14:00'})
    assert worker.is_available_if_needed('21.07', '10:00-13:30') is True


def test_worker_is_not_available_if_needed_during_exact_time_frame():
    worker = Worker(name='John Doe', availability={'21.07': '8:00-10:00'}, worse_availability={'21.07': '10:00-14:00'})
    assert worker.is_available_if_needed('21.07', '15:00-17:00') is False


def test_worker_is_not_available_if_needed_during_that_day():
    worker = Worker(name='John Doe', availability={'21.07': '8:00-10:00'}, worse_availability={'21.07': '10:00-14:00'})
    assert worker.is_available_if_needed('22.07', '12:00-13:00') is False


def test_worker_is_available_if_needed_but_overlap_time_frame():
    worker = Worker(name='John Doe', availability={'21.07': '8:00-10:00'}, worse_availability={'21.07': '10:00-14:00'})
    assert worker.is_available_if_needed('21.07', '13:30-17:00') is True


def test_str_to_time_standard_conversion():
    assert Worker._str_to_time("13:30") == time(13, 30)


def test_str_to_time_midnight():
    assert Worker._str_to_time("00:00") == time(00, 00)


def test_str_to_time_invalid_input():
    with pytest.raises(ValueError):
        assert Worker._str_to_time("John:Doe") == time(00, 00)
    with pytest.raises(ValueError):
        assert Worker._str_to_time("John Doe") == time(00, 00)
