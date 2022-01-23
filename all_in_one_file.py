import random
from math import sqrt
from time import sleep
from tkinter import *
import matplotlib.pyplot as plt

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



class Dot:
    diameter = 5
    goal_position = [400, 10, 10]


    def __init__(self, root, main_window, x=400, y=550, color='red'):
        self.brain = Brain(1000)

        self.fitness = 0
        self.position = [x, y]
        self.velocity = [0, 0]
        self.acceleration = [0, 0]
        self.main_window = main_window
        self.root = root
        self.dot = main_window.create_oval(x, y, x+Dot.diameter, y+Dot.diameter, fill=color)

        self.reached_goal = False
        self.dead = False


    def move(self):
        if self.brain.size > self.brain.step:
            self.acceleration = self.brain.directions[self.brain.step]
            self.brain.step += 1

        else:
            dead = True

        update_array(self.velocity, self.acceleration, limit=True)
        update_array(self.position, self.velocity)

    
    def update(self):
        if not self.dead and not self.reached_goal:
            self.move()

            if self.position[0]+Dot.diameter >= self.root.winfo_width() or self.position[0]<0:
                self.dead = True

            if self.position[1]+Dot.diameter >= self.root.winfo_height() - 15 or self.position[1]<0:
                self.dead = True

            if calc_distance(self.position, Dot.goal_position) < 5:
                self.reached_goal = True
                self.dead = True
            
            if not self.dead and not self.reached_goal:
                self.main_window.move(self.dot, self.velocity[0], self.velocity[1])  


    def calc_fitness(self):
        if self.reached_goal:
            self.fitness = 1 / 8 + 10000 / self.brain.step ** 2
        else:
            distance = calc_distance(self.position, Dot.goal_position)
            if distance != 0:
                self.fitness = 1 / distance ** 2
            else:
                self.fitness = 1


    def baby(self, best_color='red'):
        new_baby = Dot(self.root, self.main_window, color=best_color)  # can add color change randomly
        new_baby.brain = self.brain.clone()
        return new_baby

            

def update_array(list1, list2, limit=False, lim_val=10):
    for i in range(len(list1)):
        if limit:
            if -lim_val < list1[i]+list2[i] < lim_val:
                list1[i] += list2[i]
            elif list1[i]+list2[i] > lim_val:
                list1[i] = lim_val
            elif list1[i]+list2[i] < -lim_val:
                list1[i] = -lim_val
        else:
            list1[i] += list2[i]


def calc_distance(pos1, pos2):
    return sqrt((pos1[0] + Dot.diameter/2 - pos2[0])**2 + (pos1[1] + Dot.diameter/2 - pos2[1])**2)
  

class Population:
    min_step = 1000
    gen = 1

    def __init__(self, root, main_window, size):
        self.size = size
        self.dots = [Dot(root, main_window) for x in range(size)]
    
    def update(self):
        for dot in self.dots:
            if dot.brain.step > Population.min_step:
                dot.dead = True
            else:
                dot.update()

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
      


def plot_progress(data, on=True):
    if on:
        plt.clf()
        plt.plot(data, 'bo-')
        plt.show(block=False)

   
WIDTH = 800
HEIGHT = 600

plt.figure(2)
root = Tk()
root.title('Dot AI')

main_window = Canvas(root, height=HEIGHT, width=WIDTH, bg='white')
curr_gen_label = Label(root, text=f'Generation: {Population.gen}')
curr_gen_label.pack()
main_window.pack()

goal = main_window.create_oval(Dot.goal_position[0], Dot.goal_position[1], Dot.goal_position[0]+Dot.goal_position[2], Dot.goal_position[1]+Dot.goal_position[2], fill='blue')
population = Population(root, main_window, 1000)  # population is 1000
root.update()
total_reached_goal = []


while True:
    if not population.is_all_dots_dead():
        population.update()
        root.update()
        sleep(0.01)

    else:
        main_window.delete('all')
        goal = main_window.create_oval(Dot.goal_position[0], Dot.goal_position[1], Dot.goal_position[0]+Dot.goal_position[2], Dot.goal_position[1]+Dot.goal_position[2], fill='blue')
        population.calc_fitnesses()
        total_reached_goal.append(population.how_many())
        population.natural_selection()
        population.mutate_population()
        curr_gen_label.config(text=f'Generation: {Population.gen} |  Dots Reached Goal:  {total_reached_goal[Population.gen-2]} / 1000')
        plot_progress(total_reached_goal)

        
# yeah this was a great learning experience maybe i'll add some comments for myself later
