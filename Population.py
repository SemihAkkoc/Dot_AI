from Dot import Dot
import random

class Population:
    min_step = 1000
    gen = 1

    def __init__(self, root, main_window, size):
        self.size = size
        self.dots = [Dot(root, main_window) for x in range(size)]
    
    def update(self, obsticals):
        for dot in self.dots:
            if dot.brain.step > Population.min_step:
                dot.dead = True
            else:
                dot.update(obsticals)

    def calc_fitnesses(self):
        for dot in self.dots:
            dot.calc_fitness()

    def is_all_dots_dead(self):
        for dot in self.dots:
            if not dot.dead:
                return False
        return True

    def natural_selection(self):
        self.new_dots = []
        self.calc_fitness_sum()
        self.set_best_dot()

        self.new_dots.append(self.best_dot.baby(best_color='green'))
        for i in range(1, self.size):
            # select parent based on fitness
            parent = self.select_parent()
            # get baby from them
            self.new_dots.append(parent.baby())

        self.dots = self.new_dots[:]
        Population.gen += 1

    
    def calc_fitness_sum(self):
        self.fitness_sum = 0
        for dot in self.dots:
            self.fitness_sum += dot.fitness

    def select_parent(self):
        rand = random.uniform(0, self.fitness_sum)
        running_sum = 0

        for dot in self.dots:
            running_sum += dot.fitness
            if (running_sum > rand):
                return dot

    def mutate_population(self):
        for i in range(1, self.size):
            self.dots[i].brain.mutate()


    def set_best_dot(self):
        max_fitness = 0
        for dot in self.dots:
            if dot.fitness > max_fitness:
                max_fitness = dot.fitness
                self.best_dot = dot
        
        if self.best_dot.reached_goal:
            Population.min_step = self.best_dot.brain.step

    def how_many(self):
        count = 0
        for dot in self.dots:
            if dot.reached_goal:
                count += 1
        return count

