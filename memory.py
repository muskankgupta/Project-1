class Memory:
    def __init__(self):
        self.memory = []

    def store(self, entry):
        self.memory.append(entry)

    def get_all(self):
        return self.memory