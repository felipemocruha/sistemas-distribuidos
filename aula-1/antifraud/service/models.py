import tensorflow as tf
import numpy as np
#import pandas as pd
from keras.models import Sequential
from keras.layers import Dense


antifraud_model = AntifraudModel()

class AntifraudModel:
    def __init__(self):
        self.model = Sequential()
        self.model.add(Dense(4, input_shape=input_shape))
        self.model.add(Dense(30, activation="sigmoid"))
        self.model.add(Dense(10, activation="sigmoid"))
        self.model.add(Dense(1, activation="softmax"))
        self.model.compile(
            loss="categorical_crossentropy",
            optimizer="adam",
            metrics=["accuracy"],
        )

    def approve(self, data):
        input_dict = {
            name: tf.convert_to_tensor([value]) for name, value in data.items()
        }
        predictions = model.predict(input_dict)

        return predictions[0][0]
