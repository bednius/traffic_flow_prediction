import nn_module
from datetime import datetime
from datetime import timedelta
from DBRepository import check_data_quality, connect, load_data
import numpy as np
import itertools
import operator
import collections
import matplotlib.pyplot as plt

begh = '00:00'
endh = '23:59'
datetime_pattern = '%Y-%m-%d %H:%M'


def accumulate_min_max(l):
    a = []
    max_d = collections.defaultdict(int)
    min_d = collections.defaultdict(int)
    for key, number in l:
        if not key in a:
            a.append(key)
        max_d[key] = max(number, max_d[key])
        min_d[key] = min(number, 5000 if min_d[key] == 0 else min_d[key])
    return [(f, min_d[f], max_d[f]) for f in a]


def process_data(rows):
    i = 0
    features = np.zeros(shape=(len(rows), 5))
    labels = np.empty(len(rows))
    for row in rows:
        # train_data[i][0] = row[3] # time

        features[i][0] = np.cos(row[1] * (2. * np.pi / 1440))
        features[i][1] = np.sin(row[1] * (2. * np.pi / 1440))

        features[i][2] = np.cos(row[0] * (2. * np.pi / 7))
        features[i][3] = np.sin(row[0] * (2. * np.pi / 7))
        # train_data[i][row[1] + 1] = 1
        weekend = 0.0
        if row[0] == 0 or row[0] == 6:
            weekend = 1.0
        elif row[0] == 5:
            weekend = 0.1
        features[i][4] = weekend
        labels[i] = row[2]
        i += 1
    return features, labels


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


def plot_prediction(model, sensorId, startDate, endDate):
    test_rows = generate_test_rows()
    test_processed_data, _ = process_data(rows)
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

    print(str(start_datetime))

    rows = load_data(15, str(start_datetime), str(end_datetime))

    rows_tpl = [((x, y), z) for (x, y, z) in rows]

    for sensorId in range(sensorIds[0], sensorIds[1]):
        model = nn_module.create_model()
        rows = load_data(sensorId, str(start_datetime), str(end_datetime))
        features, labels = process_data(rows)
        model = nn_module.train_model(model, features, labels, patience=100, epochs=500)

        plot_prediction(model, sensorId)








