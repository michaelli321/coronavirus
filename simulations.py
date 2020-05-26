from Person import Person
import random
import math
import matplotlib.pyplot as plt
import numpy as np

def initialize(n, min_x, max_x, min_y, max_y, mask_simulation, bias):
    people = []

    for i in range(n):
        random_location = (random.random() * max_x, random.random() * max_y)
        mask = 0

        if mask_simulation:
            mask = random.choice([0, 1])

        person = Person(random_location, 0, mask)

        if i < bias * n:
            person.infection_time = 0
            person.state = 1

        people.append(person)

    return people

def distance(p1, p2):
    return math.sqrt((p1.x_loc - p2.x_loc)**2 + (p1.y_loc - p2.y_loc)**2)

def infect(p1, p2):
    return (-0.06 * (distance(p1, p2)) + .99)

def infect_mask(p1, p2):
    return 0

def update_infection(p1, p2, i):
    if random.random() < infect(p1, p2):
        p2.state = 1
        p2.infection_time = i if p2.infection_time == -1 else p2.infection_time
        print("new person infected %d", i)

    return p2

def update_recovery(p1, i):
    if p1.infection_time >= 0 and i - p1.infection_time == 20160:
        if random.random() < .05: # scale by num_infected
            p1.state = -1
            print("new person dead %d", i)
        else:
            p1.state = 2
            print("new person recoverd %d", i)

    return p1


if __name__=="__main__":
    max_x = 5280
    max_y = 5280
    n = 1200
    bias = .05
    timesteps = 130000 # hours 2160

    people = initialize(n, 0, max_x, 0, max_y, 0, bias)
    # fig = plt.figure(figsize=(20,15))
    # fig = plt.figure(figsize=(15, 10))
    # ax = fig.add_subplot(111)

    # plt.ion()
    # fig.show()
    # fig.canvas.draw()

    for time in range(timesteps):
        infected_locs = np.array([[person.x_loc, person.y_loc] for person in people if person.state == 1])
        immune_locs = np.array([[person.x_loc, person.y_loc] for person in people if person.state == 2])
        healthy_locs = np.array([[person.x_loc, person.y_loc] for person in people if person.state == 0])
        dead_locs = np.array([[person.x_loc, person.y_loc] for person in people if person.state == -1])

        infected_indices = [i for i in range(len(people)) if people[i].state == 1]
        healthy_indices = [i for i in range(len(people)) if people[i].state == 0]


        # plt.axis([0, max_x, 0, max_y])
        if time % 60 == 0:
            plt.clf()
            if len(healthy_locs):
                plt.plot(healthy_locs[:,0], healthy_locs[:,1], 'go')
            if len(immune_locs):
                plt.plot(immune_locs[:,0], immune_locs[:,1], 'x')
            if len(infected_locs):
                plt.plot(infected_locs[:,0], infected_locs[:,1], 'ro')
            if len(dead_locs):
                plt.plot(dead_locs[:,0], dead_locs[:,1], 'ko')
            plt.axis([0, max_x, 0, max_y])
            plt.pause(0.01)

        for infected in infected_indices:
            for healthy in healthy_indices:
                people[healthy] = update_infection(people[infected], people[healthy], time)

        for i in range(len(people)):
            people[i].update_velocity(0, max_x, 0, max_y)
            people[i] = update_recovery(people[i], time)
            people[i].move()
