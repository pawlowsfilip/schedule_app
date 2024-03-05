import pytest
from unittest.mock import patch
from worker_manager import Worker_Manager
from worker import Worker


@patch('builtins.input', side_effect=['exit'])
def test_init_with_no_workers(mock_input):
    wm = Worker_Manager()
    assert len(wm.workers_list) == 0
    assert wm.position_priorities == {}


def test_init_with_workers():
    w1 = Worker("John Doe", {'21.07': '9:00-17:00'})
    w2 = Worker("Doe John", {'22.07': '9:00-17:00'})
    wm = Worker_Manager(w1, w2)
    assert len(wm.workers_list) == 2
    assert wm.workers_list[0].name == "John Doe"
    assert wm.workers_list[1].name == "Doe John"


# make_workers tests__________________________________
def test_make_workers():
    w1 = Worker("John Doe", {'21.07': '9:00-17:00'})
    w2 = Worker("Doe John", {'22.07': '9:00-17:00'})
    wm = Worker_Manager(w1, w2)
    assert wm.make_workers(w1, w2) == [w1, w2]


@patch('builtins.input', side_effect=['John Doe', 'Manager', {'21.07': '9:00-17:00'}, {'21.07': '18:00-12:00'}, 'exit'])
def test_make_workers_custom_input(mock_input):
    workers_list = Worker_Manager.make_workers()
    assert len(workers_list) == 1
    assert isinstance(workers_list[0], Worker)
    assert workers_list[0].name == "John Doe"
    assert workers_list[0].position == "Manager"
    assert workers_list[0].availability == {'21.07': '9:00-17:00'}
    assert workers_list[0]._worse_availability == {'21.07': '18:00-12:00'}


# set_position_priorities tests_______________________
def test_set_position_priorities_correctly():
    w1 = Worker("John Doe", {'21.07': '9:00-17:00'})
    wm = Worker_Manager(w1)
    position_priorities = {'CEO': 1, 'Manager': 2}
    wm.set_position_priorities(position_priorities)
    assert wm.position_priorities == position_priorities


def test_set_position_priorities_empty():
    w1 = Worker("John Doe", {'21.07': '9:00-17:00'})
    wm = Worker_Manager(w1)
    position_priorities = {}
    wm.set_position_priorities(position_priorities)
    assert wm.position_priorities == position_priorities


def test_set_position_priorities_updated_correctly():
    w1 = Worker("John Doe", {'21.07': '9:00-17:00'})
    wm = Worker_Manager(w1)
    initial_priorities = {'CEO': 1, 'Manager': 2}
    updated_priorities = {'CEO': 2, 'Manager': 1}

    wm.set_position_priorities(initial_priorities)
    assert wm.position_priorities == initial_priorities

    wm.set_position_priorities(updated_priorities)
    assert wm.position_priorities == updated_priorities


# get_sorted_workers_by_position_priority tests_______
def test_get_sorted_workers_by_position_priority_correctly():
    w1 = Worker("John Doe", {'21.07': '9:00-17:00'}, position="Manager")
    w2 = Worker("Doe John", {'22.07': '9:00-17:00'}, position="CEO")
    wm = Worker_Manager(w1, w2)
    wm.set_position_priorities({"CEO": 1, "Manager": 2})

    assert wm.get_sorted_workers_by_position_priority() == [w2, w1]


def test_get_sorted_workers_by_position_priority_without_positions():
    w1 = Worker("John Doe", {'21.07': '9:00-17:00'})
    w2 = Worker("Doe John", {'22.07': '9:00-17:00'})
    wm = Worker_Manager(w1, w2)
    wm.set_position_priorities({"CEO": 1, "Manager": 2})

    assert wm.get_sorted_workers_by_position_priority() == [w1, w2]


# get_available_workers tests_________________________
def test_get_available_workers_one_worker_available():
    w1 = Worker("John Doe", {'21.07': '8:00-9:00'})
    w2 = Worker("Doe John", {'22.07': '10:00-15:00'})
    wm = Worker_Manager(w1, w2)
    day = '21.07'
    time_frame = '8:30-8:50'

    assert wm.get_available_workers(day, time_frame) == [w1]


def test_get_available_workers_no_workers_available_because_wrong_day():
    w1 = Worker("John Doe", {'21.07': '8:00-9:00'})
    w2 = Worker("Doe John", {'21.07': '8:00-9:00'})
    wm = Worker_Manager(w1, w2)
    day = '22.07'
    time_frame = '8:00-9:00'

    assert wm.get_available_workers(day, time_frame) == []


def test_get_available_workers_all_workers_available():
    w1 = Worker("John Doe", {'21.07': '8:00-9:00'})
    w2 = Worker("Doe John", {'21.07': '8:00-9:00'})
    wm = Worker_Manager(w1, w2)
    day = '21.07'
    time_frame = '8:00-9:00'

    assert wm.get_available_workers(day, time_frame) == [w1, w2]


def test_get_available_workers_edge_case():
    w1 = Worker("John Doe", {'21.07': '8:00-9:00'})
    wm = Worker_Manager(w1)
    day = '21.07'
    time_frame = '8:00-9:00'

    assert wm.get_available_workers(day, time_frame) == [w1]


def test_get_available_workers_overlap_time_frame():
    w1 = Worker("John Doe", {'21.07': '8:00-9:00'})
    wm = Worker_Manager(w1)
    day = '21.07'
    time_frame = '8:00-10:00'

    assert wm.get_available_workers(day, time_frame) == []


def test_get_available_workers_available_for_multiple_time_frames():
    w1 = Worker("John Doe", {'21.07': '8:00-9:00,10:00-12:00'})
    wm = Worker_Manager(w1)
    day = '21.07'
    time_frame1 = '8:00-9:00'
    time_frame2 = '10:00-12:00'

    assert wm.get_available_workers(day, time_frame1) == [w1]
    assert wm.get_available_workers(day, time_frame2) == [w1]


def test_get_available_workers_available_for_multiple_days():
    w1 = Worker("John Doe", {'21.07': '8:00-9:00', '22.07': '8:00-9:00'})
    wm = Worker_Manager(w1)
    day1 = '21.07'
    day2 = '22.07'
    time_frame = '8:00-9:00'

    assert wm.get_available_workers(day1, time_frame) == [w1]
    assert wm.get_available_workers(day2, time_frame) == [w1]


# remove_worker tests_________________________________
def test_remove_worker_correctly_one_worker():
    w1 = Worker("John Doe", {'21.07': '8:00-9:00', '22.07': '8:00-9:00'})
    wm = Worker_Manager(w1)

    assert wm.remove_worker(w1) is True and len(wm.workers_list) == 0


def test_remove_worker_correctly_two_workers():
    w1 = Worker("John Doe", {'21.07': '8:00-9:00', '22.07': '8:00-9:00'})
    w2 = Worker("John Doe", {'21.07': '8:00-9:00', '22.07': '8:00-9:00'})
    wm = Worker_Manager(w1, w2)

    assert wm.remove_worker(w1) is True and len(wm.workers_list) == 1


# get_days tests______________________________________
def test_get_days_correctly_from_one_day():
    w1 = Worker("John Doe", {'21.07': '8:00-9:00'})
    wm = Worker_Manager(w1)

    assert wm.get_days() == w1._availability.keys()


def test_get_days_correctly_from_two_day():
    w1 = Worker("John Doe", {'21.07': '8:00-9:00', '22.07': '8:00-9:00'})
    wm = Worker_Manager(w1)

    assert wm.get_days() == w1._availability.keys()


def test_get_days_correctly_from_no_availability():
    w1 = Worker("John Doe", {})
    wm = Worker_Manager(w1)

    assert wm.get_days() == w1._availability.keys()


# get_hours tests_____________________________________
def test_get_hours_for_specific_day_single_worker():
    w1 = Worker("John Doe", {'21.07': '8:00-9:00'})
    wm = Worker_Manager(w1)

    assert wm.get_hours('21.07') == '8:00-9:00'


def test_get_hours_for_unavailable_day():
    w1 = Worker("John Doe", {'21.07': '8:00-9:00'})
    wm = Worker_Manager(w1)

    assert wm.get_hours('22.07') is None
