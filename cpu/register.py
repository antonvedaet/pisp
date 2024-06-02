class Register:
    def __init__(self):
        self.value = 0

    def load(self, value):
        self.value = value

    def read(self):
        return self.value