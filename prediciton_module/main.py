import nn_module
from datetime import datetime
from datetime import timedelta
from DBRepository import check_data_quality, connect, load_data, persist_predictions
import numpy as np
import itertools
import operator
import collections
import matplotlib.pyplot as plt

from nn_test import make_tests
from utils import process_data

begh = '00:14'
endh = '23:59'
datetime_pattern = '%Y-%m-%d %H:%M'


def accumulate_min_max(l):
    a = []
    max_d = collections.defaultdict(int)
    min_d = collections.defaultdict(int)
    for key, number in l:
        if key not in a:
            a.append(key)
        max_d[key] = max(number, max_d[key])
        min_d[key] = min(number, 5000 if min_d[key] == 0 else min_d[key])
    return [(f, min_d[f], max_d[f]) for f in a if f[1] % 15 == 14]


def get_mins_max(l):
    mins_max = accumulate_min_max(l)
    mins_max.sort(key=lambda tup: tup[0])

    mins_maxx = [el for el in mins_max if el[0][0] != 0]
    mins_maxx.extend([el for el in mins_max if el[0][0] == 0])
    return mins_maxx


def generate_test_rows():
    days = [1, 2, 3, 4, 5, 6, 0]
    mins = [x for x in range(14, 1440, 15)]
    rows = np.zeros(shape=(672, 3))
    i = 0
    for d in days:
        for m in mins:
            rows[i] = (d, m, 0)
            i += 1
    return rows


def plot_prediction(model, sensorId, startDate, endDate, mins_max):
    test_rows = generate_test_rows()
    test_processed_data, _ = process_data(test_rows)
    train_labels = model.predict(test_processed_data).flatten()
    days_of_week = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
    x = np.empty(len(train_labels))
    for i in range(len(train_labels)):
        x[i] = i
    y = train_labels
    frequency = 96
    plt.ylabel('Total volume')
    plt.xlabel('Days of week')
    plt.xticks(x[48::frequency], days_of_week)
    # plt.yticks(np.arange(y.min(), y.max(), 0.005))
    plt.plot(x, y)
    plt.plot(x, [el[1] for el in mins_maxx])
    plt.plot(x, [el[2] for el in mins_maxx])
    plt.grid(axis='y', linestyle='-')
    plt.title('Sensor id {}, time period: {} to {}'.format(str(sensorId), '2016-04-11', '2016-04-17'))
    plt.savefig('one_week_volume_9005.png')
    plt.show()
    pass


if __name__ == '__main__':

    # num_hidden_layers = 3
    # dims_hidden_layers = [50, 100, 50]
    # optimizer='rms',
    # metrics,
    # loss,
    # input_dim

    connect()
    startTrainDate = '2016-09-02'
    endTrainDate = '2016-11-20'

    start_datetime = datetime.strptime(startTrainDate + ' ' + begh, datetime_pattern)
    end_datetime = datetime.strptime(endTrainDate + ' ' + endh, datetime_pattern)

    sensorIds = [15, 16]


    for sensorId in range(sensorIds[0], sensorIds[1]):
        # prepare data

        make_tests()

        rows = load_data(15, str(start_datetime), str(end_datetime))

        rows_tpl = [((x, y), z) for (x, y, z) in rows]

        mins_max = get_mins_max(rows_tpl)

        ##



        model = nn_module.create_model()
        rows = load_data(sensorId, str(start_datetime), str(end_datetime))
        features, labels = process_data(rows)
        model = nn_module.train_model(model, features, labels, patience=100, epochs=500)
        nn_module.save_model(model, start_datetime, end_datetime, sensorId)
        #model = nn_module.load_model('./uploads/15_2016-11-21 23:59:00.h5')
        plot_prediction(model, sensorId, startTrainDate, endTrainDate, mins_maxx)

        test_rows = generate_test_rows()
        test_processed_data, _ = process_data(test_rows)
        predict_labels = model.predict(test_processed_data).flatten()

        # persist_predictions(sensorId, start_datetime, mins_maxx, predict_labels)

