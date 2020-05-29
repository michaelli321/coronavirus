import random

class Person:
    def __init__(self, location, state, mask):
        self.x_loc = location[0]
        self.y_loc = location[1]
        self.velocity = [(random.random()*3.5)-1.75, (random.random()*3.5)-1.75] # hours
        # self.velocity = [(random.random()*7.3)-3.65, (random.random()*7.3)-3.65] # minutes
        self.state = state
        self.mask = mask
        self.infection_time = -1
        self.home = 0

    def move(self):
        self.x_loc = self.x_loc + self.velocity[0]
        self.y_loc = self.y_loc + self.velocity[1]

    def update_velocity(self, min_x, max_x, min_y, max_y):
        if self.x_loc + self.velocity[0] < min_x or self.x_loc + self.velocity[0] > max_x:
            self.velocity[0] = -1 * self.velocity[0]

        if self.y_loc + self.velocity[1] > max_y or self.y_loc + self.velocity[1] < min_y:
            self.velocity[1] = -1 * self.velocity[1]
