from tkinter import *
from time import sleep
from Population import Population
from Dot import Dot
import matplotlib.pyplot as plt


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

