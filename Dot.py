from math import sqrt
from Brain import Brain
from time import sleep


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
            self.dead = True

        update_array(self.velocity, self.acceleration, limit=True)
        update_array(self.position, self.velocity)

    
    def update(self, obsticals):
        if not self.dead and not self.reached_goal:
            self.move()

            if self.position[0]+Dot.diameter >= self.root.winfo_width() or self.position[0]<0:
                self.dead = True

            if self.position[1]+Dot.diameter >= self.root.winfo_height() - 15 or self.position[1]<0:
                self.dead = True
                
            for obstical in obsticals.obsticals:
                no_zone = self.main_window.coords(obstical)
                if no_zone[0] < self.position[0] < no_zone[2] and no_zone[1] < self.position[1] < no_zone[3]:
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
