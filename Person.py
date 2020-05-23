import random

class Person:
    def __init__(self, location, state, survival_rate, mask):
        self.x_loc = location[0]
        self.y_loc = location[1]
        self.velocity = (random.randint(-5, 5), random.randint(-5, 5))
        self.state = state
        self.survival_rate = survival_rate
        self.mask = mask

    def move(self):
        self.x_loc = self.x_loc + self.velocity[0]
        self.y_loc = self.y_loc + self.velocity[1]

    def update_velocity(self, min_x, max_x, min_y, max_y):
        if self.x_loc + self.velocity[0] < min_x and self.x_loc + self.velocity[0] > max_x: 
            self.velocity[0] = -1 * self.velocity[0]
        
        if self.y_loc + self.velocity[1] > max_y and self.y_loc + self.velocity[1] < min_y:
            self.velocity[1] = -1 * self.velocity[1]
            