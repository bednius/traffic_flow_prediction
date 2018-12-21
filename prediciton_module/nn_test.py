import pandas as pd
import numpy as np
from datetime import datetime, timedelta

import nn_module
from DBRepository import load_data, connect
from utils import process_data
import matplotlib.pyplot as plt

begh = '00:14'
endh = '23:59'
datetime_pattern = '%Y-%m-%d %H:%M'


def plot_full_week(y_test, y_predict, sensorId, start_datetime_test, end_datetime_test, dirr='./plots/'):
    days_of_week = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
    x = np.empty(len(y_test))
    for i in range(len(y_test)):
        x[i] = i
    y = y_test
    frequency = 96
    plt.ylabel('Total volume')
    plt.xlabel('Days of week')
    plt.xticks(x[48::frequency], days_of_week)
    # plt.yticks(np.arange(y.min(), y.max(), 0.005))
    true_vals, = plt.plot(x, y, label='True values')
    pred_vals, = plt.plot(x, y_predict, label='Predict values')
    plt.legend(handles=[true_vals, pred_vals])
    plt.grid(axis='y', linestyle='-')
    title = 'Sensor id {}, time period: {} to {}'.format(str(sensorId), str(start_datetime_test),
                                                         str(end_datetime_test))

    plt.title(title)
    plt.savefig('{}{}.png'.format(dirr, title))
    plt.show()
    pass


def plot_history(history, dirr='./plots/'):
    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('Mean Abs Error')
    plt.plot(history.epoch, np.array(history.history['mean_absolute_error']),
             label='Train Error')
    plt.plot(history.epoch, np.array(history.history['val_mean_absolute_error']),
             label='Val Error')
    plt.legend()
    plt.savefig('{}{}.png'.format(dirr, 'mae'))
    plt.ylim([0, 100])
    plt.show()

    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('Mean Square Error')
    plt.plot(history.epoch, np.array(history.history['mean_squared_error']),
             label='Train Error')
    plt.plot(history.epoch, np.array(history.history['val_mean_squared_error']),
             label='Val Error')
    plt.legend()
    plt.savefig('{}{}.png'.format(dirr, 'mse'))
    plt.ylim([0, 2000])
    plt.show()


def make_tests():
    sensorId = 90

    connect()
    startTrainDate = '2016-09-02'
    endTrainDate = '2016-11-13'

    start_datetime_train = datetime.strptime(startTrainDate + ' ' + begh, datetime_pattern)
    end_datetime_train = datetime.strptime(endTrainDate + ' ' + endh, datetime_pattern)

    start_datetime_test = end_datetime_train + timedelta(minutes=15)
    end_datetime_test = end_datetime_train + timedelta(days=7)

    X_train, y_train = process_data(load_data(sensorId, start_datetime_train, end_datetime_train))
    X_test, y_test = process_data(load_data(sensorId, start_datetime_test, end_datetime_test))

    losses = ['mae', 'mse', 'logcosh']
    optimizers = ['adam', 'rmsprop']
    nums_of_hidden_layers = [2, 3, 4]
    dimss_of_hidden_layers = [[50, 50], [50, 100, 50], [100, 200, 100], [50, 100, 100, 50]]

    loss = losses[0]
    optimizer = optimizers[0]
    dims_of_hidden_layers = dimss_of_hidden_layers[0]
    num_hidden_layers = len(dims_of_hidden_layers)

    f = open("./plots/results.txt", "a+")

    for dims_of_hidden_layers in dimss_of_hidden_layers:
        for optimizer in optimizers:
            for loss in losses:
                num_hidden_layers = len(dims_of_hidden_layers)
                test_params = '{}_{}_{}_{}'.format(loss, optimizer, num_hidden_layers, dims_of_hidden_layers);
                folder_path = './plots/{}/'.format(test_params)
                import os

                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)

                model = nn_module.create_model(loss=loss, optimizer=optimizer,
                                               num_hidden_layers=num_hidden_layers,
                                               dims_hidden_layers=dims_of_hidden_layers)

                model, history, train_time = nn_module.train_model(model, X_train, y_train, patience=100, epochs=1000)
                # nn_module.save_model(model, start_datetime_train, end_datetime_train, sensorId)
                scores = model.evaluate(X_test, y_test)

                plot_history(history, folder_path)

                print('Loss function: {}'.format(scores[0]))
                print('Mean Absolute Error: {}'.format(scores[1]))
                print('Mean Squared Error: {}'.format(scores[2]))
                print('Training Time: {}'.format(train_time))

                f.write('loss function_optimizer_numHiddenLayers_dims\n')
                f.write('{}\n'.format(test_params))
                f.write('Loss function: {}\n'.format(scores[0]))
                f.write('Mean Absolute Error: {}\n'.format(scores[1]))
                f.write('Mean Squared Error: {}\n'.format(scores[2]))
                f.write('Training Time: {}\n'.format(train_time))
                f.write('---------------------------------------------\n')

                y_predict = model.predict(X_test).flatten()

                plot_full_week(y_test, y_predict, sensorId, start_datetime_test, end_datetime_test, folder_path)

    ##

    #####

    # model = nn_module.load_model('./uploads/15_2016-11-21 23:59:00.h5')
    # plot_prediction(model, sensorId, startTrainDate, endTrainDate, mins_maxx)

    # test_rows = generate_test_rows()
    # test_processed_data, _ = process_data(test_rows)
    # predict_labels = model.predict(test_processed_data).flatten()


make_tests()
