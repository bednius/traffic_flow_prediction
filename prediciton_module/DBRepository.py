import psycopg2

import time


def connect(dbname='tfpv2', user='tfp', host='localhost', password='tfp'):
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
    except:
        print("cannot execute a query")

    rows = cur.fetchall()

    return rows[0][0] / max_measurments

# load_data(9005, '2016-04-11 00:14:00.000000', '2016-04-17 23:59:00.000000')
