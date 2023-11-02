import os
import keras.layers
import tensorflow as tf
import numpy as np

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "1"
tf.keras.utils.disable_interactive_logging()


class Node:
    x_pos, y_pos, x_max, y_max, steps = 0, 0, 0, 0, 0

    model = object
    field = object

    BLOCKED_FIELD_VALUE = -1

    INPUT_SIZE = 11
    OUTPUT_SIZE = 4
    N_HIDDEN = 64
    DROPOUT = 0.3

    # TODO: relocate
    LOSS_FN = tf.keras.losses.SparseCategoricalCrossentropy()
    OPTIMIZER = tf.keras.optimizers.legacy.Adam(learning_rate=0.001)

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
        self.model.add(keras.layers.Dense(self.N_HIDDEN,
                                          name="dense_layer_0",
                                          activation="relu"))
        self.model.add(keras.layers.Dropout(self.DROPOUT))
        self.model.add(keras.layers.Dense(self.N_HIDDEN,
                                          name="dense_layer_1",
                                          activation="relu"))
        self.model.add(keras.layers.Dropout(self.DROPOUT))
        self.model.add(keras.layers.Dense(self.OUTPUT_SIZE, name="dense_output_layer"))

    def get_x_pos(self):
        return self.x_pos

    def get_y_pos(self):
        return self.y_pos

    # @tf.function(input_signature=(tf.TensorSpec(shape=[None], dtype=tf.float32)))
    def do_step(self):
        temp = self.get_input_data()

        step = tf.convert_to_tensor([temp], dtype=tf.float32)
        self.last_step = step

        prediction = self.model(step)
        predicted_class = tf.argmax(prediction, axis=-1)
        move = predicted_class.numpy()

        if move[0] == 0:
            self.move_up()
        elif move[0] == 1:
            self.move_down()
        elif move[0] == 2:
            self.move_right()
        elif move[0] == 3:
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

    @tf.function
    def get_input_data(self):
        field_x_max_value = self.field.get_x_max() - 1
        field_y_max_value = self.field.get_y_max() - 1

        # TODO: put calculations for surroundings into separate service
        data = np.array([self.x_pos / field_x_max_value,
                         self.y_pos / field_y_max_value,
                         0 if ((self.x_pos != field_x_max_value)
                               and self.field.get_matrix()[self.x_pos + 1][self.y_pos] == 0)
                         else self.BLOCKED_FIELD_VALUE,
                         0 if (self.x_pos != 0
                               and self.field.get_matrix()[self.x_pos - 1][self.y_pos] == 0)
                         else self.BLOCKED_FIELD_VALUE,
                         0 if ((self.y_pos != field_y_max_value)
                               and self.field.get_matrix()[self.x_pos][self.y_pos + 1] == 0)
                         else self.BLOCKED_FIELD_VALUE,
                         0 if (self.y_pos != 0
                               and self.field.get_matrix()[self.x_pos][self.y_pos - 1] == 0)
                         else self.BLOCKED_FIELD_VALUE,
                         self.field.get_steps(),
                         0,
                         1,
                         0,
                         1])

        return data

    @tf.function
    def train_model(self):

        with tf.GradientTape() as tape:
            temp = self.get_input_data()
            test2 = tf.convert_to_tensor([temp], dtype=tf.float32)
            test = self.model(test2)
            loss_value = self.get_loss_value(test)



            # gradients = tape.gradient(self.__get_loss_value(), self.model.trainable_variables)
            # self.OPTIMIZER.apply_gradients(zip(gradients, self.model.trainable_variables))

        grads = tape.gradient(loss_value, self.model.trainable_weights)

        #optimizer.build(variables)


        self.OPTIMIZER.apply_gradients(zip(grads, self.model.trainable_weights))


    # Demo loss value funktion
    @tf.function
    def get_loss_value(self, test):
        return tf.square(test * (self.x_pos / self.x_max))

