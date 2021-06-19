from random import random, randint, choice

import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


class AntifraudModel:
    def __init__(self):
        self.model = self._get_model()

    def _get_model(self):
        self.init_options = [
            tf.keras.initializers.Orthogonal(gain=random()),
            tf.keras.initializers.RandomNormal(stddev=random()),
            tf.keras.initializers.RandomNormal(mean=random(), stddev=random()),
            tf.keras.initializers.RandomUniform(minval=-0.05, maxval=random()),
            tf.keras.initializers.TruncatedNormal(mean=random(), stddev=random()),
        ]
        init = choice(self.init_options)

        model = Sequential()
        model.add(Dense(4, kernel_initializer=init, input_shape=(1, 4)))
        model.add(Dense(30, kernel_initializer=init, activation="sigmoid"))
        model.add(Dense(10, kernel_initializer=init, activation="sigmoid"))
        model.add(Dense(1, kernel_initializer=init, activation="sigmoid"))
        model.compile(
            loss="mse",
            optimizer="adam",
            metrics=["accuracy"],
        )

        return model

    def approve(self, data):
        observation = np.expand_dims(np.array([*data.values()]), 0)
        predictions = self.model.predict(observation)
        self.model = self._get_model()

        return predictions[0][0]


antifraud_model = AntifraudModel()
