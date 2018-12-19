from datetime import timedelta

import psycopg2

import time


def connect(dbname='tfpv2', user='tfp', host='localhost', password='tfp'):
    global conn
    try:
        conn = psycopg2.connect("dbname={} user={} host={} password={}".format(dbname, user, host, password))
    except:
        print("Cannot connect to database")
        exit(1)

    global cur
    cur = conn.cursor()
    pass


def load_data(sensorId, startDate, endDate):
    query = """SELECT
  CAST(EXTRACT(DOW FROM m.datetime) as INT) as day_of_weak,
  CAST(EXTRACT(hours from m.datetime) * 60 + EXTRACT(minutes FROM m.datetime) as int) as time,
  m.total_volume
FROM measurement m
WHERE
  m.sensor_object_id = {} and
  m.total_volume notnull and
  m.datetime between '{}' and '{}'
order by m.datetime"""

    try:
        cur.execute(query.format(sensorId, startDate, endDate))
    except:
        print("cannot execute a query")

    rows = cur.fetchall()
    return rows


def check_data_quality(sensorId, startDate, endDate):
    max_measurments = ((endDate - startDate).days + 1) * 96

    query = '''select count(*)
from measurement m
where m.sensor_object_id = {} and
      m.datetime between '{}' and '{}' '''

    try:
        cur.execute(query.format(sensorId, startDate, endDate))
    except Exception as e:
        print("cannot execute a query, msg: {}".format(str(e)))

    rows = cur.fetchall()

    return rows[0][0] / max_measurments


# load_data(9005, '2016-04-11 00:14:00.000000', '2016-04-17 23:59:00.000000')

def persist_predictions(sensorId, startDate, mins_max, results):
    query = '''insert into prediction(s_datetime, max_historical_volume, min_historical_volume, total_volume, s_sensor_object_id)
    values ('{}', {}, {}, {}, {});'''
    p_datetime = startDate
    for mmtpl, r in zip(mins_max, results):
        p_datetime = p_datetime + timedelta(minutes=15)
        try:
            cur.execute(query.format(str(p_datetime), mmtpl[2], mmtpl[1], r, sensorId))
            conn.commit()
        except Exception as e:
            print("cannot execute a query, msg: {}".format(str(e)))


