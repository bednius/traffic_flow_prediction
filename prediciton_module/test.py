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

# try:
#     conn = psycopg2.connect("dbname='tfpv2' user='tfp' host='localhost' password='tfp'")
# except:
#     print("I am unable to connect to the database")
#
# cur = conn.cursor()
# try:
#     cur.execute("""SELECT
#   m.sensor_object_id,
#   CAST(EXTRACT(DOW FROM m.datetime) as INT) as day_of_weak,
#   m.total_volume,
#   CAST(EXTRACT(hours from m.datetime) * 60 + EXTRACT(minutes FROM m.datetime) as int) as time
# FROM measurement m
# WHERE
#  m.sensor_object_id between 9025 and 9025 and
#   m.total_volume notnull and
#   m.datetime between '2015-01-01 00:14:00.000000' and '2015-03-19 23:59:00.000000'
# order by m.datetime""")
# except:
#     print("cannot execute a query")
#
# rows = cur.fetchall()
#
# # for row in rows:
# #     print(row)
#
# print(tf.__version__)
#
# train_data = np.zeros(shape=(len(rows), 4))
# train_labels = np.empty(len(rows))
#
# i = 0
# for row in rows:
#     # train_data[i][0] = row[3] # time
#
#     train_data[i][0] = np.sin(row[3] * (2. * np.pi / 1439))
#     train_data[i][1] = np.cos(row[3] * (2. * np.pi / 1439))
#
#     train_data[i][2] = np.sin(row[1] * (2. * np.pi / 6))
#     train_data[i][3] = np.cos(row[1] * (2. * np.pi / 6))
#     # train_data[i][row[1] + 1] = 1
#     train_labels[i] = row[2]
#     i += 1
#
# print(train_data)

x_val = np.empty(7)
y_val = np.empty(7)
days_of_week = ['NIEDZIELA', 'PONIEDZIAŁEK', 'WTOREK', 'ŚRODA', 'CZWARTEK', 'PIĄTEK', 'SOBOTA']

for i in range(0, 7):
    x_val[i] = np.cos(i * (2. * np.pi / 7))
    y_val[i] = np.sin(i * (2. * np.pi / 7))

an = np.linspace(0, 2 * np.pi, 100)

plt.subplot(111)
plt.plot(np.cos(an), np.sin(an))
plt.axis('equal')
plt.axis([-1.5, 1.5, -1.5, 1.5])
plt.scatter(x_val, y_val)
for i, txt in enumerate(days_of_week):
    plt.annotate(txt, (x_val[i], y_val[i]))




# plt.title('dni', fontsize=10)
#
# plt.subplot(224)
# plt.plot(3*np.cos(an), 3*np.sin(an))
# plt.axis('equal')
# plt.axis([-3, 3, -3, 3])
# plt.plot([0, 4], [0, 4])
# plt.title('still equal after adding line', fontsize=10)

# plt.show()

plt.savefig('dni_tygodnia.png')

plt.show()












print(x_val, y_val)

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
  m.sensor_object_id between 9025 and 9025 and
  m.total_volume notnull and
  m.datetime between '2015-03-23 00:14:00.000000' and '2015-03-29 23:59:00.000000'
order by m.datetime""")
except:
    print("cannot execute a query")

rows = cur.fetchall()

test_data = np.zeros(shape=(len(rows), 5))
test_labels = np.empty(len(rows))

i = 0
for row in rows:
    test_labels[i] = row[2]
    i = i + 1

data = {
    # 'dates': dates,
    'volume': test_labels,
}
df = pd.DataFrame(data, columns=['volume'])
# df.groupby("dates").mean().plot()
df.plot()
# df.plot(xticks=dates)
# plt.xticks(dates)
plt.show()

plt.plot(test_labels)
plt.savefig('example_week_flow.png')
plt.show()




# try:
#     cur.execute("""SELECT
#   m.sensor_object_id,
#   CAST(EXTRACT(DOW FROM m.datetime) as INT) as day_of_weak,
#   m.total_volume,
#   CAST(EXTRACT(hours from m.datetime) * 60 + EXTRACT(minutes FROM m.datetime) as int) as time
# FROM measurement m
# WHERE
#   m.sensor_object_id between 9024 and 9024 and
#   m.total_volume notnull and
#   m.datetime between '2015-03-20 00:14:00.000000' and '2015-03-31 23:59:00.000000'
# order by m.datetime""")
# except:
#     print("cannot execute a query")
#
# rows = cur.fetchall()
#
# test_data = np.zeros(shape=(len(rows), 8))
# test_labels = np.empty(len(rows))
#
# i = 0
# for row in rows:
#     test_data[i][0] = row[3]
#     test_data[i][row[1] + 1] = 1
#     test_labels[i] = row[2]
#     i += 1
#
# mean = train_data[0].mean(axis=0)
# std = train_data[0].std(axis=0)
#
# train_data[0] = (train_data[0] - mean) / std
# test_data[0] = (test_data[0] - mean) / std
#
# print(train_data)
#
# print(train_data[0])
#
# model = keras.models.load_model("my_model.h5")
#
# [loss, mae] = model.evaluate(test_data, test_labels, verbose=0)
#
# # model.save('my_model_9025.h5')  # creates a HDF5 file 'my_model.h5'
#
# print("Testing set Mean Abs Error: {:7.2f}".format(mae))
#
#
# def plot_history(history):
#     plt.figure()
#     plt.xlabel('Epoch')
#     plt.ylabel('Mean Abs Error')
#     plt.plot(history.epoch, np.array(history.history['mean_absolute_error']),
#              label='Train Loss')
#     plt.plot(history.epoch, np.array(history.history['val_mean_absolute_error']),
#              label='Val loss')
#     plt.legend()
#     # plt.ylim([0, 5])
#     plt.show()
#
#
# # plot_history(history)
#
# test_predictions = model.predict(test_data).flatten()
#
# plt.scatter(test_labels, test_predictions)
# plt.xlabel('True Values')
# plt.ylabel('Predictions')
# plt.axis('equal')
# plt.xlim(plt.xlim())
# plt.ylim(plt.ylim())
# _ = plt.plot([-100, 100], [-100, 100])
# plt.show()
#
# data = {
#     # 'dates': dates,
#     # 'test':test_labels[200:300],
#     'test': test_labels,
#     # 'predictions':test_predictions[200:300]
#     'predictions': test_predictions
# }
# df = pd.DataFrame(data, columns=['test', 'predictions'])
# # df.groupby("dates").mean().plot()
# df.plot()
# # df.plot(xticks=dates)
# # plt.xticks(dates)
# plt.show()
