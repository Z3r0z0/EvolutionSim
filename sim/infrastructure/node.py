import random


class Node:
    x_pos, y_pos, x_max, y_max = 0, 0, 0, 0

    field = object

    def __init__(self, x, y, x_max, y_max, field):
        self.x_pos = x
        self.y_pos = y
        self.x_max = x_max
        self.y_max = y_max
        self.field = field

    def get_x_pos(self):
        return self.x_pos

    def get_y_pos(self):
        return self.y_pos

    def do_step(self):
        # TODO: implement neuronal brain

        move = random.randint(0, 4)

        if move == 0:
            self.move_up()
        elif move == 1:
            self.move_down()
        elif move == 2:
            self.move_right()
        elif move == 3:
            self.move_left()

        return self.x_pos, self.y_pos

    def move_up(self):
        if self.y_pos < (self.y_max - 1):
            if self.field[self.x_pos][(self.y_pos + 1)] == 0:
                self.y_pos += 1

    def move_down(self):
        if self.y_pos > 0:
            if self.field[self.x_pos][(self.y_pos - 1)] == 0:
                self.y_pos -= 1

    def move_right(self):
        if self.x_pos < (self.x_max - 1):
            if self.field[(self.x_pos + 1)][self.y_pos] == 0:
                self.x_pos += 1

    def move_left(self):
        if self.x_pos > 0:
            if self.field[(self.x_pos - 1)][self.y_pos] == 0:
                self.x_pos -= 1
