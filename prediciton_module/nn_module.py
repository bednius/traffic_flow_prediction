import time

import numpy as np
from keras.regularizers import l2

from tensorflow import keras
import tensorflow as tf


def create_model(num_hidden_layers=3, dims_hidden_layers=None, optimizer=None, metrics=None, loss='mse', input_dim=5):
    if metrics is None:
        metrics = ['mae']
    if dims_hidden_layers is None:
        dims_hidden_layers = [50, 100, 50]

    layers = np.empty(num_hidden_layers + 2)
    layers[0] = keras.layers.Dense(input_dim, activation=tf.nn.relu, input_shape=(input_dim, 0))
    layers[num_hidden_layers + 1] = keras.layers.Dense(1)
    for i in range(num_hidden_layers):
        layers[i + 1] = keras.layers.Dense(dims_hidden_layers[i], activation=tf.nn.relu, kernel_regularizer=l2(0.001))

    model = keras.Sequential(layers)

    model.compile(optimizer=optimizer,
                  loss=loss,
                  metrics=metrics)

    return model


def train_model(model, features, labels, patience=500, epochs=1000):
    class print_progress(keras.callbacks.Callback):
        def on_epoch_end(self, epoch, logs):
            if epoch % 100 == 0:
                print((epoch / epochs) * 100)

    early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=patience)

    start = time.time()
    print('Model training started')
    history = model.fit(features, labels, epochs=epochs,
                        validation_split=0.2, verbose=0,
                        callbacks=[early_stop, print_progress()])
    end = time.time()
    print('Training Time: {}'.format(end - start))
    return model

def save_model(model, startDate, endDate, sensorId):
    #filename = '{}_{}.h5'.format(endDate + )
    #keras.save
    pass