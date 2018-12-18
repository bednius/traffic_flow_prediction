import numpy as np


def convert(rows):
    features = np.zeros(shape=(len(rows), 5))
    labels = np.empty(len(rows))

    i = 0
    for row in rows:
        features[i][0] = np.cos(row[2] * (2. * np.pi / 1440))
        features[i][1] = np.sin(row[2] * (2. * np.pi / 1440))

        features[i][2] = np.cos(row[0] * (2. * np.pi / 7))
        features[i][3] = np.sin(row[0] * (2. * np.pi / 7))

        weekend = 0.0
        if row[0] == 0 or row[0] == 6:
            weekend = 1.0
        elif row[0] == 5:
            weekend = 0.2
        features[i][4] = weekend
        labels[i] = row[1]
        i += 1

    return features, labels
