from datetime import datetime, time


class Worker:
    def __init__(self, name, availability, worse_availability=None, position=None):
        self.name = name
        self._availability = availability
        self._worse_availability = worse_availability
        self.position = position

    def __str__(self):
        return f"Name: {self.name}, Position: {self.position}, Availability: {self._availability}, Worse availability: {self._worse_availability}"

    def get_name(self):
        return self.name

    def get_position(self):
        return self.position

    def get_availability(self):
        return self._availability

    def get_worse_availability(self):
        return self._worse_availability

    def is_available(self, required_day, required_time):
        if required_day in self._availability:
            day_availability = self._process_availability(self._availability[required_day])
            required_start_str, required_end_str = required_time.split('-')
            required_start = self._str_to_time(required_start_str)
            required_end = self._str_to_time(required_end_str)

            for worker_start, worker_end in day_availability:
                if self._is_fully_covered(worker_start, worker_end, required_start, required_end):
                    return True
            return False
        else:
            return False

    def is_available_if_needed(self, required_day, required_time):
        if required_day in self._worse_availability:
            day_availability = self._process_availability(self._worse_availability[required_day])
            required_start_str, required_end_str = required_time.split('-')
            required_start = self._str_to_time(required_start_str)
            required_end = self._str_to_time(required_end_str)

            for worker_start, worker_end in day_availability:
                if self._is_fully_covered(worker_start, worker_end, required_start, required_end):
                    return True
            return False
        else:
            return False

    @staticmethod
    def _str_to_time(time_str):
        return datetime.strptime(time_str, "%H:%M").time()

    @staticmethod
    def _is_fully_covered(worker_start, worker_end, required_start, required_end):
        return worker_start <= required_start and worker_end >= required_end

    @staticmethod
    def _time_frame_split(time_frame):
        if not isinstance(time_frame, str):
            raise ValueError("Time frame must be a string.")
        if '-' not in time_frame or len(time_frame.split('-')) != 2:
            raise ValueError("Invalid time frame format. Use 'HH:MM-HH:MM'.")
        start, end = time_frame.split('-')
        return start, end

    def _process_availability(self, availability_str):
        if not availability_str:
            return []

        scopes = availability_str.split(',')
        time_tuples = []

        for scope in scopes:
            start, end = self._time_frame_split(scope)
            start_time = self._str_to_time(start)
            end_time = self._str_to_time(end)
            time_tuple = (start_time, end_time)
            time_tuples.append(time_tuple)

        return time_tuples

    @property
    def availability(self):
        return self._availability


