import random


class Record:
    def __init__(self, key):
        self.key = key
        self.mass = random.random() * 50
        self.heat = random.random() * 50
        self.delta_temp = random.uniform(-1.0, 1.0) * 50
        self.energy = self.mass*self.heat*self.delta_temp
