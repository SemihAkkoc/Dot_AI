import random


class Brain:
    def __init__(self, size):
        self.directions = []
        self.size = size
        self.step = 0
        self.randomize(size)

    def randomize(self, size):
        for i in range(size):
            x = random.randint(-5,5)
            y = random.randint(-5,5)
            self.directions.append((x, y))
    
    def clone(self):
        clone_brain = Brain(self.size)
        clone_brain.directions = self.directions[:]
        return clone_brain

    def mutate(self):
        mutation_rate = 0.001
        for i in range(self.size):
            rand = random.random()
            if rand < mutation_rate:
                x = random.randint(-5,5)
                y = random.randint(-5,5)
                self.directions[i] = (x, y)
