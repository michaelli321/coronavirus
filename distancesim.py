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
    return -0.0008 + 0.5 * np.exp(-0.27 * distance(p1, p2))
    # return (-0.01 * (distance(p1, p2)) + .25)

def update_infection(p1, p2, i):
    if p1.state == 1 and p2.state == 0:
        if random.random() < infect(p1, p2):
            p2.state = 1
            p2.infection_time = i if p2.infection_time == -1 else p2.infection_time
    elif p1.state == 0 and p1.state == 1:
        if random.random() < infect(p1, p2):
            p1.state = 1
            p1.infection_time = i if p1.infection_time == -1 else p1.infection_time
        # print("new person infected %d", i)

    return p1, p2

def update_recovery(p1, i):
    if p1.infection_time >= 0 and i - p1.infection_time == 336:
        if random.random() < .05: # scale by num_infected
            p1.state = -1
            # print("new person dead %d", i)
        else:
            p1.state = 2
            # print("new person recoverd %d", i)

    return p1


if __name__=="__main__":
    max_x = 324
    max_y = 324
    n = 100
    bias = .06
    timesteps = 600 # 130000 # hours 2160

    people = initialize(n, 0, max_x, 0, max_y, 0, bias)

    healthy_time = []
    infected_time = []
    recovered_time = []
    dead_time = []

    for time in range(timesteps):
        infected_locs = np.array([[person.x_loc, person.y_loc] for person in people if person.state == 1])
        immune_locs = np.array([[person.x_loc, person.y_loc] for person in people if person.state == 2])
        healthy_locs = np.array([[person.x_loc, person.y_loc] for person in people if person.state == 0])
        dead_locs = np.array([[person.x_loc, person.y_loc] for person in people if person.state == -1])

        infected_indices = [i for i in range(len(people)) if people[i].state == 1]
        healthy_indices = [i for i in range(len(people)) if people[i].state == 0]

        num_healthy = len(healthy_locs)
        num_infected = len(infected_locs)
        num_recovered = len(immune_locs)
        num_dead = len(dead_locs)

        # plt.axis([0, max_x, 0, max_y])
        if time % 1 == 0:
            plt.clf()
            if num_healthy:
                plt.plot(healthy_locs[:,0], healthy_locs[:,1], 'go')
            if num_recovered:
                plt.plot(immune_locs[:,0], immune_locs[:,1], 'bo')
            if num_infected:
                plt.plot(infected_locs[:,0], infected_locs[:,1], 'ro')
            if num_dead:
                plt.plot(dead_locs[:,0], dead_locs[:,1], 'ko')
            plt.axis([0, max_x, 0, max_y])
            plt.pause(0.001)

        if time == 0 or num_healthy != healthy_time[-1][1] or time == timesteps - 1:
            healthy_time.append([time, num_healthy])
        if time == 0 or num_infected != infected_time[-1][1] or time == timesteps - 1:
            infected_time.append([time, num_infected])
        if time == 0 or num_recovered != recovered_time[-1][1] or time == timesteps - 1:
            recovered_time.append([time, num_recovered])
        if time == 0 or num_dead != dead_time[-1][1] or time == timesteps - 1:
            dead_time.append([time, num_dead])

        print("%d healthy %d infected %d recovered %d dead %d" % (time, num_healthy,
            num_infected, num_recovered, num_dead))

        changed_inds = set()

        for i in range(len(people)):
            for j in range(i+1, len(people)):
                people[i], people[j] = update_infection(people[i], people[j], time)

                if math.sqrt((people[i].x_loc+people[i].velocity[0] - people[j].x_loc-people[j].velocity[0])**2 + (people[i].y_loc+people[i].velocity[1] - people[j].y_loc-people[j].velocity[1])**2) <= 6:
                    if i not in changed_inds and j not in changed_inds: # and random.random() < .8:
                        if people[i].x_loc < people[j].x_loc:
                            people[i].update_velocity(0, max_x, 0, max_y, 1)
                            people[j].update_velocity(0, max_x, 0, max_y, 1)
                            changed_inds.add(i)
                            changed_inds.add(j)

            if i not in changed_inds:
                people[i].update_velocity(0, max_x, 0, max_y)

        
        for i in range(len(people)):
            people[i].move()
            people[i] = update_recovery(people[i], time)


    print(healthy_time)
    healthy_time = np.array(healthy_time)
    infected_time = np.array(infected_time)
    recovered_time = np.array(recovered_time)
    dead_time = np.array(dead_time)
    plt.close()
    plt.xlabel('Time (Hours)')
    plt.ylabel('# of People')
    plt.title('Spread of Coronavirus w/Social Distancing')
    plt.plot(healthy_time[:, 0], healthy_time[:, 1], "g", label='# Healthy')
    plt.plot(infected_time[:, 0], infected_time[:, 1], "r", label='# Infected')
    plt.plot(recovered_time[:, 0], recovered_time[:, 1], "b", label="# Recovered")
    # plt.plot(dead_time[:, 0], dead_time[:, 1], "k")
    plt.show()
