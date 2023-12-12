class Fifo():
    def __init__(self, init_vals: list):
        self.values = init_vals

    def append(self, value: int | str | float):
        self.values = self.values.append(value)

    def remove(self):
        first_elem = self.values.pop(0)
        return first_elem

    def get(self):
        return self.values

