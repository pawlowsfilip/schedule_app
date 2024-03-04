from datetime import datetime, time
from worker import Worker
import pytest


# _init tests____________________________________
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


def test_init_with_all_arguments_but_worker_unavailable():
    worker = Worker(name='John Doe', availability={'21.07': ''}, worse_availability={'21.07': ''},
                    position='Manager')
    assert worker.get_name() == 'John Doe'
    assert worker.get_availability() == {'21.07': ''}
    assert worker.get_worse_availability() == {'21.07': ''}
    assert worker.get_position() == 'Manager'


def test_get_name():
    worker = Worker(name='John Doe', availability={'21.07': '8:00-10:00'}, worse_availability={'21.07': '10:00-14:00'},
                    position='Manager')
    assert worker.get_name() == "John Doe"


def test_get_position():
    worker = Worker(name='John Doe', availability={'21.07': '8:00-10:00'}, worse_availability={'21.07': '10:00-14:00'},
                    position='Manager')
    assert worker.get_position() == "Manager"


def test_get_availability():
    worker = Worker(name='John Doe', availability={'21.07': '8:00-10:00'}, worse_availability={'21.07': '10:00-14:00'},
                    position='Manager')
    assert worker.get_availability() == {'21.07': '8:00-10:00'}


def test_get_worse_availability():
    worker = Worker(name='John Doe', availability={'21.07': '8:00-10:00'}, worse_availability={'21.07': '10:00-14:00'},
                    position='Manager')
    assert worker.get_worse_availability() == {'21.07': '10:00-14:00'}

# _is_available tests____________________________
@pytest.mark.parametrize("availability, required_day, required_time, expected",[
    ({"21.07": "8:00-10:00"}, "21.07", "8:00-9:00", True),  # Available for entire timeframe
    ({"21.07": "8:00-10:00"}, "21.07", "7:00-9:00", False),  # Available for part of the time frame
    ({"21.07": "8:00-10:00"}, "21.07", "10:00-11:00", False),  # Not available - with availability
    ({"21.07": ""}, "21.07", "10:00-11:00", False),  # Not available - without availability
    ({"21.07": "8:00-10:00"}, "21.07", "8:00-10:00", True),  # Exact match of availability with required time frame
    ({"21.07": "8:00-9:00"}, "21.07", "6:00-7:00", False),  # Time frame outside the availability
    ({"22.07": "8:00-9:00"}, "21.07", "8:00-9:00", False),  # Required time frame on different day
])
def test_worker_is_available(availability, required_day, required_time, expected):
    worker = Worker(name='John Doe', availability=availability)
    assert worker.is_available(required_day, required_time) == expected


# _is_available_if_needed tests__________________
@pytest.mark.parametrize("worse_availability, required_day, required_time, expected",[
    ({"21.07": "8:00-10:00"}, "21.07", "8:00-9:00", True),  # Available for entire timeframe
    ({"21.07": "8:00-10:00"}, "21.07", "7:00-9:00", False),  # Available for part of the time frame
    ({"21.07": "8:00-10:00"}, "21.07", "10:00-11:00", False),  # Not available - with availability
    ({"21.07": ""}, "21.07", "10:00-11:00", False),  # Not available - without availability
    ({"21.07": "8:00-10:00"}, "21.07", "8:00-10:00", True),  # Exact match of availability with required time frame
    ({"21.07": "8:00-9:00"}, "21.07", "6:00-7:00", False),  # Time frame outside the availability
    ({"22.07": "8:00-9:00"}, "21.07", "8:00-9:00", False),  # Required time frame on different day
])
def test_worker_is_available_if_needed(worse_availability, required_day, required_time, expected):
    worker = Worker(name='John Doe', availability={'21.07': ''}, worse_availability=worse_availability)
    assert worker.is_available_if_needed(required_day, required_time) == expected


# _str_to_time tests_____________________________
def test_str_to_time_standard_conversion():
    assert Worker._str_to_time("13:30") == time(13, 30)


def test_str_to_time_midnight():
    assert Worker._str_to_time("00:00") == time(00, 00)


def test_str_to_time_invalid_input():
    with pytest.raises(ValueError):
        assert Worker._str_to_time("John:Doe") == time(00, 00)
    with pytest.raises(ValueError):
        assert Worker._str_to_time("John Doe") == time(00, 00)


# _is_overlap tests______________________________
@pytest.mark.parametrize("worker_start, worker_end, required_start, required_end, expected", [
    ("8:00", "10:00", "8:00", "10:00", True),  # Exact match
    ("7:00", "11:00", "8:00", "10:00", True),  # Worker's availability includes required time frame
    ("8:00", "9:00", "8:30", "10:00", False),  # Partial overlap at the end
    ("9:00", "11:00", "8:00", "9:30", False),  # Partial overlap at the start
    ("11:00", "12:00", "8:00", "9:00", False)  # No overlap
])
def test_is_fully_covered(worker_start, worker_end, required_start, required_end, expected):
    worker_start = Worker._str_to_time(worker_start)
    worker_end = Worker._str_to_time(worker_end)
    required_start = Worker._str_to_time(required_start)
    required_end = Worker._str_to_time(required_end)
    assert Worker._is_fully_covered(worker_start, worker_end, required_start, required_end) == expected


# _time_frame_split tests________________________
def test_time_frame_split_correctly():
    time_frame = "12:00-13:00"
    assert Worker._time_frame_split(time_frame) == ("12:00", "13:00")


def test_time_frame_split_one_hour():
    time_frame = "12:00"
    with pytest.raises(ValueError):
        assert Worker._time_frame_split(time_frame)


# _process_availability tests____________________
def test_process_availability_correct_one_frame():
    worker = Worker(name='John Doe', availability={})
    availability_str = '8:00-10:00'
    expected_output = [(worker._str_to_time('8:00'), worker._str_to_time('10:00'))]
    assert worker._process_availability(availability_str) == expected_output


def test_process_availability_correct_more_than_one_frame():
    worker = Worker(name='John Doe', availability={})
    availability_str = '8:00-10:00,11:00-12:00'
    expected_output = [(worker._str_to_time('8:00'), worker._str_to_time('10:00')),
                       (worker._str_to_time('11:00'), worker._str_to_time('12:00'))]
    assert worker._process_availability(availability_str) == expected_output


def test_process_availability_empty_string():
    worker = Worker(name='John Doe', availability={})
    availability_str = ''
    expected_output = []
    assert worker._process_availability(availability_str) == expected_output


def test_process_availability_incorrect():
    worker = Worker(name='John Doe', availability={})
    availability_str = '9:00-10:00'
    expected_output = [(worker._str_to_time('8:00'), worker._str_to_time('10:00'))]
    assert worker._process_availability(availability_str) != expected_output


def test_process_availability_incorrect_one_hour():
    worker = Worker(name='John Doe', availability={})
    availability_str = 'invalid input'
    with pytest.raises(ValueError):
        assert worker._process_availability(availability_str)


def test_process_availability_incorrect_not_a_string():
    worker = Worker(name='John Doe', availability={})
    availability_str = 9    # int doesn't have a 'split'
    with pytest.raises(AttributeError):
        assert worker._process_availability(availability_str)
