from datetime import datetime, time


class Worker:
    def __init__(self, name, availability, worse_availability=None, position=None):
        self.name = name
        self._availability = availability
        self._worse_availability = worse_availability
        self.position = position

    def is_available(self, day, time):    # wyciagnij klucz i wartosc z availability (słownika) i porównaj z day i time
        pass

    @staticmethod
    def _str_to_time(time_str):
        return datetime.strptime(time_str, "%H:%M").time()

    @staticmethod
    def _is_overlap(worker_start, worker_end, required_start, required_end):
        return (worker_start <= required_end) and (worker_end >= required_start)

    @staticmethod
    def _time_frame_split(time_frame):
        start, end = time_frame.split('-')
        return start, end

    def _process_availability(self, availability_str):
        scopes = availability_str.split(',')
        time_tuples = []

        for scope in scopes:
            start, end = self._time_frame_split(scope)
            start_time = self._str_to_time(start)
            end_time = self._str_to_time(end)
            time_tuple = (start_time, end_time)
            time_tuples.append(time_tuple)

        return time_tuples

    def _availability(self):
        return self._process_availability(self._availability.keys())  # wyciagnac klucz z availability i zrobic prywatnie (idk)

    def _is_available(self, availability_str, required_start, required_end):
        return any(self._is_overlap(worker_start, worker_end, self._str_to_time(required_start),
                                    self._str_to_time(required_end))
                   for worker_start, worker_end in self._availability(availability_str))
