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
  m.datetime between '2016-04-01 00:14:00.000000' and '2016-09-10 23:59:00.000000'
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
    # train_data[i][row[1] + 1] = 1
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
  m.datetime between '2016-09-11 00:00:00.000000' and '2016-09-18 23:59:59.000000'
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

model = keras.models.load_model("first_bad_model_9002.h5")

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
    'predictions': test_predictions,
    'test': test_labels,
}
df = pd.DataFrame(data, columns=['test', 'predictions'])
# df.groupby("dates").mean().plot()
df.plot()
# df.plot(xticks=dates)
# plt.xticks(dates)
plt.show()