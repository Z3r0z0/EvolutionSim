import random as rand
import numpy as np

from sim.infrastructure.node import Node


class Grid:
    x_max, y_max = 0, 0
    creatures = 0

    steps_init = 0
    steps = 0

    matrix = [0][0]
    nodes = []

    def __init__(self, x_max, y_max, creature_count, steps):
        self.x_max = x_max
        self.y_max = y_max
        self.creatures = creature_count

        self.steps_init = steps
        self.steps = steps

        self.matrix = [[0 for y in range(self.y_max)] for x in range(self.x_max)]

        self.matrix = np.array(self.matrix)

        for i in range(self.creatures):
            x, y = self.__get_random_free_location()
            self.matrix[x][y] = i + 1
            self.nodes.append(Node(x, y, self.x_max, self.y_max, self))

    def step(self):
        for i in range(self.creatures):
            selected_node = self.nodes[i]
            x_old = selected_node.get_x_pos()
            y_old = selected_node.get_y_pos()

            x, y = self.nodes[i].do_step()
            if x_old != x or y_old != y:
                self.matrix[x_old][y_old] = 0
                self.matrix[x][y] = i

        return self.matrix

    def get_matrix(self):
        return self.matrix

    def get_steps(self):
        return self.steps

    def get_x_max(self):
        return self.x_max

    def get_y_max(self):
        return self.y_max

    def train_creatures(self):
        self.matrix = [[0 for y in range(self.y_max)] for x in range(self.x_max)]

        for i in range(self.creatures):
            self.nodes[i].train_model()

            x, y = self.__get_random_free_location()
            self.matrix[x][y] = i + 1

            self.nodes[i].x_pos = x
            self.nodes[i].y_pos = y

    def __get_random_free_location(self):
        while 1:
            x = rand.randint(0, self.x_max - 1)
            y = rand.randint(0, self.y_max - 1)
            if self.matrix[x][y] == 0:
                return x, y
