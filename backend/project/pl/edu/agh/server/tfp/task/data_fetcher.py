import requests
import traceback
import json
import sys
import os
import datetime
from django_cron import CronJobBase, Schedule
import django
from celery.schedules import crontab
from celery.task import periodic_task
from pl.edu.agh.server.tfp.models import Measurement, Sensor


class DownloadTask(object):

    def __init__(self,
                 startDate=datetime.date(day=1, month=2, year=2016),
                 finishDate=datetime.date(day=31, month=3, year=2016)
                 ):
        urlStartDate = startDate.strftime("%d%m%Y")
        urlFinishDate = finishDate.strftime("%d%m%Y")
        self.url = "http://webtris.highwaysengland.co.uk/api/v1/reports/{}/to/{}/daily?sites=".format(urlStartDate,
                                                                                                 urlFinishDate)

    startDate = datetime.date(2016, 2, 1)
    finishDate = datetime.date(2016, 3, 31)

    params = "&page=1&page_size=200"
    current_path = os.path.dirname(os.path.abspath(__file__)) + "/reportsv  3"

    # radom initialization
    actualDate = datetime.date(1900, 1, 1)
    actualFile = None

    def make_request(self, url):
        return requests.get(url)

    def _get_int_value(self, string):
        return int(string) if string else 0

    def save_data(self, id, json):
        global actualFile
        rows = json["Rows"]

        sensor = None
        if len(rows) > 0:
            try:
                sensor = Sensor.objects.get(pk=id)
            except Sensor.DoesNotExist:
                sensor = Sensor(id=id, name=rows[0]["Site Name"])
                sensor.save()
        else:
            sys.stderr.write('No data for sensor {}'.format(id))

        for row in rows:
            avg_mph = self._get_int_value(row["Avg mph"])
            total_volume = self._get_int_value(row["Total Volume"])
            status = Measurement.SUCCESSFUL if total_volume > 0 else Measurement.NO_DATA

            measurement = Measurement(sensor_object=sensor, datetime=row["Report Date"].replace('00:00:00', row["Time Period Ending"]),
                                      avg_mph=avg_mph, total_volume=total_volume, status=status)
            measurement.save()

    def iterate_over_links(self, id, json_links):
        for link in json_links:
            if link["rel"] == "nextPage":
                response = self.make_request(link["href"])
                if response.status_code == 200:
                    json_data = response.json()
                    # print (json_data)
                    self.save_data(id, json_data)
                    if json_data["Header"]['links']:
                        self.iterate_over_links(id, json_data["Header"]['links'])

    def main(self):
        for id in range(1, 17367):
            try:
                response = self.make_request(self.url + str(id) + self.params)
                if response.status_code == 200:

                    json_data = response.json()
                    self.save_data(id, json_data)
                    if json_data["Header"]["links"]:
                        self.iterate_over_links(id, json_data["Header"]["links"])
                else:

                    sys.stderr.write(str(id) + "\t" + response.text + "\n")
                    sys.stderr.flush()
            except KeyboardInterrupt:
                sys.exit()
            except:
                sys.stderr.write("Unexpected error:" + str(sys.exc_info()[0]))
                sys.stderr.write(traceback.format_exc())


class MyCronJob(CronJobBase):
    ALLOW_PARALLEL_RUNS = True
    RUN_EVERY_MINS = 3600  # every 60 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'my_app.my_cron_job'  # a unique code
    DownloadTask().main()

    def do(self):
        DownloadTask().main()


if __name__ == '__main__':

    #TODO configure to run DownloadTask as standalone script
    DownloadTask.main()

# @periodic_task(run_every=crontab(hour=7, minute=30, day_of_week="mon"))
# def every_monday_morning():
#     print("This is run every Monday morning at 7:30")
