import random

import keras.layers
import tensorflow as tf

class Node:
    x_pos, y_pos, x_max, y_max, steps = 0, 0, 0, 0, 0

    model = object
    field = object

    INPUT_SIZE = 7
    OUTPUT_SIZE = 4
    N_HIDDEN = 64
    DROPOUT = 0.3

    def __init__(self, x, y, x_max, y_max, field):
        self.x_pos = x
        self.y_pos = y
        self.x_max = x_max
        self.y_max = y_max
        self.field = field
        self.init_nn()

    def init_nn(self):
        self.model = tf.keras.models.Sequential()
        self.model.add(keras.layers.Dense(self.INPUT_SIZE,
                                          input_shape=(self.INPUT_SIZE,),
                                          name="dense_input_layer",
                                          activation="relu"))
        self.model.add(keras.layers.Dropout(self.DROPOUT))
        self.model.add(keras.layers.Dense(self.N_HIDDEN,
                                          name="dense_layer_1",
                                          activation="relu"))
        self.model.add(keras.layers.Dropout(self.DROPOUT))
        self.model.add(keras.layers.Dense(self.OUTPUT_SIZE, name="dense_output_layer"))

        # TODO: other loss function
        self.model.compile(optimizer="Adam", loss="categorical_crossentropy")

    def get_x_pos(self):
        return self.x_pos

    def get_y_pos(self):
        return self.y_pos

    def do_step(self):
        # TODO: implement neuronal brain

        temp = self.get_input_data()

        print(temp)
        print(temp.shape)

        # TODO: execute model
        temp_move = self.model.evaluate(temp)
        #temp_move = self.model(temp)

        print(temp_move)

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
            if self.field.get_matrix()[self.x_pos][(self.y_pos + 1)] == 0:
                self.y_pos += 1

    def move_down(self):
        if self.y_pos > 0:
            if self.field.get_matrix()[self.x_pos][(self.y_pos - 1)] == 0:
                self.y_pos -= 1

    def move_right(self):
        if self.x_pos < (self.x_max - 1):
            if self.field.get_matrix()[(self.x_pos + 1)][self.y_pos] == 0:
                self.x_pos += 1

    def move_left(self):
        if self.x_pos > 0:
            if self.field.get_matrix()[(self.x_pos - 1)][self.y_pos] == 0:
                self.x_pos -= 1

    def get_input_data(self):
        data = tf.constant([
            self.x_pos,
            self.y_pos,
            self.field.get_matrix()[self.x_pos + 1][self.y_pos],
            self.field.get_matrix()[self.x_pos - 1][self.y_pos],
            self.field.get_matrix()[self.x_pos][self.y_pos + 1],
            self.field.get_matrix()[self.x_pos][self.y_pos - 1],
            self.field.get_steps()
        ], shape=(7,))

        return data

