# TensorFlow and tf.keras
from __future__ import division, print_function
import tensorflow as tf
from tensorflow import keras
from keras.regularizers import l2
import array as arr
import pandas as pd

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt

import psycopg2

import time

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
  m.sensor_object_id between 9002 and 9002 and
  m.total_volume notnull and
  m.datetime between '2016-04-01 00:14:00.000000' and '2016-09-19 23:59:00.000000'
order by m.datetime""")
except:
    print("cannot execute a query")

rows = cur.fetchall()

# for row in rows:
#     print(row)

print(tf.__version__)

train_data = np.zeros(shape=(len(rows), 5))
train_labels = np.empty(len(rows))

i = 0
for row in rows:
    # train_data[i][0] = row[3] # time

    train_data[i][0] = np.cos(row[3] * (2. * np.pi / 1440))
    train_data[i][1] = np.sin(row[3] * (2. * np.pi / 1440))

    train_data[i][2] = np.cos(row[1] * (2. * np.pi / 7))
    train_data[i][3] = np.sin(row[1] * (2. * np.pi / 7))

    weekend = 0.0
    if row[1] == 0 or row[1] == 6:
        weekend = 1.0
    elif row[1] == 5:
        weekend = 0.2
    train_data[i][4] = weekend
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
 m.sensor_object_id between 9002 and 9002 and
  m.total_volume notnull and
  m.datetime between '2016-09-19 00:00:00.000000' and '2016-09-25 23:59:59.000000'
order by m.datetime""")
except:
    print("cannot execute a query")

rows = cur.fetchall()

test_data = np.zeros(shape=(len(rows), 5))
test_labels = np.empty(len(rows))

i = 0
for row in rows:
    # train_data[i][0] = row[3] # time

    test_data[i][0] = np.cos(row[3] * (2. * np.pi / 1440))
    test_data[i][1] = np.sin(row[3] * (2. * np.pi / 1440))

    test_data[i][2] = np.cos(row[1] * (2. * np.pi / 7))
    test_data[i][3] = np.sin(row[1] * (2. * np.pi / 7))
    # train_data[i][row[1] + 1] = 1
    weekend = 0.0
    if row[1] == 0 or row[1] == 6:
        weekend = 1.0
    elif row[1] == 5:
        weekend = 0.1
    test_data[i][4] = weekend
    test_labels[i] = row[2]
    i += 1

# mean = train_data[0].mean(axis=0)
# std = train_data[0].std(axis=0)

# train_data[0] = (train_data[0] - mean) / std
# test_data[0] = (test_data[0] - mean) / std

print(train_data)

print(train_data[0])

# train_output = train_output
# test_output = test_output


model = keras.Sequential([
    # keras.layers.Flatten(input_shape=(3, 1)),
    keras.layers.Dense(5, activation=tf.nn.relu, input_shape=(train_data.shape[1],)),
    # keras.layers.Dense(200, activation=tf.nn.relu, kernel_regularizer=l2(0.001)),
    # keras.layers.Dense(200, activation=tf.nn.relu, kernel_regularizer=l2(0.001)),
    keras.layers.Dense(100, activation=tf.nn.relu, kernel_regularizer=l2(0.001)),
    keras.layers.Dense(200, activation=tf.nn.relu, kernel_regularizer=l2(0.001)),
    keras.layers.Dense(100, activation=tf.nn.relu, kernel_regularizer=l2(0.001)),
    # keras.layers.Dense(20, activation=tf.nn.relu, activity_regularizer=l2(0.001)),
    # keras.layers.Dense(10, activation=tf.nn.relu, activity_regularizer=l2(0.001)),
    # keras.layers.Dense(3, activation=tf.nn.relu),
    # keras.layers.Dense(1, activation='linear', activity_regularizer=l2(0.001), )
    keras.layers.Dense(1)
])

# optimizer = keras.optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
# optimizer = tf.train.AdagradOptimizer(0.001)
# optimizer = tf.train.ProximalGradientDescentOptimizer(10.0)
optimizer = keras.optimizers.RMSprop()
# optimizer = tf.train.AdamOptimizer(0.01)
# optimizer = tf.train.ProximalGradientDescentOptimizer(10.0) #tf.train.ProximalGradientDescentOptimizer(0.01)
model.compile(optimizer=optimizer,
              loss='mse',
              metrics=['mae'])

# model.compile(
#     loss='kullback_leibler_divergence',
#     optimizer=optimizer,
#     metrics=['mae']
# )

# model.fit(train_input, train_output, epochs=5)

model.summary()


class PrintDot(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs):
        if epoch % 100 == 0: print('')
        print('.', end='')


early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=500)

EPOCHS = 500

start = time.time()

history = model.fit(train_data, train_labels, epochs=EPOCHS,
                    validation_split=0.2, verbose=0,
                    callbacks=[early_stop, PrintDot()])

end = time.time()

# model = keras.models.load_model("my_model.h5")


[loss, mae] = model.evaluate(test_data, test_labels, verbose=0)

model.save('my_model_9002.h5')  # creates a HDF5 file 'my_model.h5'

print("Testing set Mean Abs Error: {:7.2f}".format(mae))


def plot_history(history):
    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('Mean Abs Error')
    plt.plot(history.epoch, np.array(history.history['mean_absolute_error']),
             label='Train Loss')
    plt.plot(history.epoch, np.array(history.history['val_mean_absolute_error']),
             label='Val loss')
    plt.legend()
    plt.ylim([0, 5])
    plt.show()


plot_history(history)

test_predictions = model.predict(test_data).flatten()

plt.scatter(test_labels, test_predictions)
plt.xlabel('True Values')
plt.ylabel('Predictions')
plt.axis('equal')
plt.xlim(plt.xlim())
plt.ylim(plt.ylim())
_ = plt.plot([-100, 100], [-100, 100])
plt.show()

data = {
    # 'dates': dates,
    'test': test_labels,
    'predictions': test_predictions
}
df = pd.DataFrame(data, columns=['test', 'predictions'])
# df.groupby("dates").mean().plot()
df.plot()
# df.plot(xticks=dates)
# plt.xticks(dates)
plt.show()

print("time: ", end - start)

score = model.evaluate(test_data, test_labels)