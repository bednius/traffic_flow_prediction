from __future__ import absolute_import, division, print_function

import tensorflow as tf
from tensorflow import keras

import numpy as np

import psycopg2

try:
    conn = psycopg2.connect("dbname='tfpv2' user='tfp' host='localhost' password='tfp'")
except:
    print("I am unable to connect to the database")

cur = conn.cursor()
try:
    cur.execute("""SELECT
  m.sensor_object_id,
  CAST(EXTRACT(DOW FROM m.datetime) as INT) as day_of_weak,
  m.total_volume,
  CAST(EXTRACT(hours from m.datetime) * 60 + EXTRACT(minutes FROM m.datetime) as int) as time
FROM measurement m
WHERE
 m.sensor_object_id between 6012 and 6013 and
  m.total_volume notnull and
  m.datetime between '2015-01-01 00:14:00.000000' and '2015-02-28 23:59:00.000000'
order by m.datetime""")
except:
    print("cannot execute a query")

rows = cur.fetchall()

# for row in rows:
#     print(row)

print(tf.__version__)

train_data = np.zeros(shape=(len(rows), 3))
train_labels = np.empty(len(rows))

i = 0
for row in rows:
    train_data[i] = [row[0], row[1] + 1, row[3]]
    train_labels[i] = row[2]
    i += 1

try:
    cur.execute("""SELECT
  m.sensor_object_id,
  CAST(EXTRACT(DOW FROM m.datetime) as INT) as day_of_weak,
  m.total_volume,
  CAST(EXTRACT(hours from m.datetime) * 60 + EXTRACT(minutes FROM m.datetime) as int) as time
FROM measurement m
WHERE
  m.sensor_object_id between 6012 and 6013 and
  m.total_volume notnull and
  m.datetime between '2015-03-01 00:14:00.000000' and '2015-03-31 23:59:00.000000'
order by m.datetime""")
except:
    print("cannot execute a query")

rows = cur.fetchall()

test_data = np.zeros(shape=(len(rows), 3))
test_labels = np.empty(len(rows))

i = 0
for row in rows:
    test_data[i] = [row[0], row[1] + 1, row[3]]
    test_labels[i] = row[2]
    i += 1

mean = train_data.mean(axis=0)
std = train_data.std(axis=0)

train_data = (train_data - mean) / std
test_data = (test_data - mean) / std

# boston_housing = keras.datasets.boston_housing

# (train_data, train_labels), (test_data, test_labels) = boston_housing.load_data()
#
# # Shuffle the training set
# order = np.argsort(np.random.random(train_labels.shape))
# train_data = train_data[order]
# train_labels = train_labels[order]

print("Training set: {}".format(train_data.shape))  # 404 examples, 13 features
print("Testing set:  {}".format(test_data.shape))  # 102 examples, 13 features

print(train_data[0])  # Display sample features, notice the different scales

import pandas as pd

column_names = ['CRIM', 'ZN', 'INDUS']

df = pd.DataFrame(train_data, columns=column_names)
df.head()

# print(train_labels[0:10])  # Display first 10 entries

# Test data is *not* used when calculating the mean and std

mean = train_data.mean(axis=0)
std = train_data.std(axis=0)

for i in range(len(std)):
    if (std[i] == 'NULL'):
        std[i] = train_data[0][i]
print(std)
train_data = (train_data - mean) / std
test_data = (test_data - mean) / std

print(train_data[0])  # First training sample, normalized


def build_model():
    model = keras.Sequential([
        keras.layers.Dense(200, activation=tf.nn.relu,
                           input_shape=(train_data.shape[1],)),
        keras.layers.Dense(200, activation=tf.nn.relu),
        keras.layers.Dense(1)
    ])

    # optimizer = tf.train.RMSPropOptimizer(0.001)
    # optimizer = tf.train.ProximalGradientDescentOptimizer(1000.0)
    optimizer = keras.optimizers.Adadelta(lr=1.0, rho=0.95, epsilon=None, decay=0.0)

    model.compile(loss='mse',
                  optimizer=optimizer,
                  metrics=['mae'])
    return model


model = build_model()
model.summary()

EPOCHS = 500


# Display training progress by printing a single dot for each completed epoch
class PrintDot(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs):
        if (epoch % 100 == 0):
            print(epoch / EPOCHS * 100, "/ 100")


# Store training stats
# early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=20)
history = model.fit(train_data, train_labels, epochs=EPOCHS,
                    validation_split=0.2, verbose=0,
                    callbacks=[PrintDot()])

import matplotlib.pyplot as plt


def plot_history(history):
    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('Mean Abs Error')
    plt.plot(history.epoch, np.array(history.history['mean_absolute_error']),
             label='Train Loss')
    plt.plot(history.epoch, np.array(history.history['val_mean_absolute_error']),
             label='Val loss')
    plt.legend()
    # plt.ylim([0, 10000])
    plt.show()


plot_history(history)

[loss, mae] = model.evaluate(test_data, test_labels, verbose=0)

print("Testing set Mean Abs Error: {:7.2f}".format(mae))

test_predictions = model.predict(test_data).flatten()

plt.scatter(test_labels, test_predictions)
plt.xlabel('True Values')
plt.ylabel('Predictions')
plt.axis('equal')
plt.xlim(plt.xlim())
plt.ylim(plt.ylim())
_ = plt.plot([0, 8000], [-0, 10000])
plt.show()


