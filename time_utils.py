from datetime import datetime, time


def str_to_time(time_str):
    return datetime.strptime(time_str, "%H:%M").time()


def is_overlap(worker_start, worker_end, required_start, required_end):
    return (worker_start <= required_end) and (worker_end >= required_start)


def process_availability(availability_str):
    scopes = availability_str.split(',')
    time_tuples = []

    for scope in scopes:
        start, end = scope.split('-')
        start_time = str_to_time(start)
        end_time = str_to_time(end)
        time_tuple = (start_time, end_time)
        time_tuples.append(time_tuple)

    return time_tuples


def availability(availability_str):
    return process_availability(availability_str)


def is_available(availability_str, required_start, required_end):
    return any(is_overlap(worker_start, worker_end, required_start, required_end)
               for worker_start, worker_end in availability(availability_str))
