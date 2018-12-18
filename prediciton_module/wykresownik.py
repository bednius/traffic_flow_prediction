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
  m.sensor_object_id between 15 and 15 and
  m.total_volume notnull and
  m.datetime between '2016-10-18 00:14:00.000000' and '2016-10-25 23:29:00.000000'
order by m.datetime""")
except:
    print("cannot execute a query")

# for row in rows:
#     print(row)

rows = cur.fetchall()

train_data = np.zeros(shape=(len(rows), 5))
train_labels = np.empty(len(rows))
dates = np.empty(len(rows))

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


# data = {
#     'test': train_labels,
# }
# df = pd.DataFrame(data, columns=['test'])
# # df.groupby("dates").mean().plot()
# df.plot()

days_of_week = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
xd = np.zeros(666, dtype=np.str)

plt.xlim('xd')


# df.groupby("dates").mean().plot()
plt.plot(xd, train_labels)
plt.ylabel('Total Volume')
# df.plot(xticks=dates)
# plt.xticks(dates)
plt.show()


x = np.empty(len(train_labels))
for i in range(len(train_labels)):
    x[i] = i
y = train_labels
my_xticks = xd
frequency = 96
plt.ylabel('Total volume')
plt.xlabel('Days of week')
plt.xticks(x[48::frequency], days_of_week)
#plt.yticks(np.arange(y.min(), y.max(), 0.005))
plt.plot(x, y)
plt.grid(axis='y', linestyle='-')
plt.title('Sensor id {}, time period: {} to {}'.format(str(9005), '2016-04-11', '2016-04-17'))
plt.savefig('one_week_volume_9005.png')
plt.show()






