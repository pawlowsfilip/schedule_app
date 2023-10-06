class Worker:
    def __init__(self, name, availability, worse_availability=None, position=None):
        self.name = name
        self.availability = availability
        self.worse_availability = worse_availability
        self.position = position
