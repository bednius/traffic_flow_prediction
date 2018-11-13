from django.template import loader
from django.http import HttpResponse
import datetime

from pl.edu.agh.server.tfp.models import Sensor, Measurement
from pl.edu.agh.server.tfp.sample_data.predictions import PREDICTIONS
from pl.edu.agh.server.tfp.sample_data.sensors import SENSORS
from pl.edu.agh.server.tfp.util.templates import INDEX, HOME_TEMPLATE, CHART
from pl.edu.agh.server.tfp.task.data_fetcher import DownloadTask


def index(request):
    template = loader.get_template(HOME_TEMPLATE)
    query_result = Sensor.objects.exclude(longitude__isnull=True)

    sensors = query_result[:100]
    first_datetime = datetime.datetime(year=2016, month=3, day=1)
    last_datetime = datetime.datetime(year=2016, month=3, day=2)

    print (sensors)

    template_data = [[s.id, s.latitude, s.longitude] for s in sensors]

    results = []

    # for i, sensor in enumerate(sensors):
    #     result = Measurement.objects.filter(sensor_object=sensor,
    #                                         datetime__range=(first_datetime, last_datetime))
    #     result_volume = [{r.datetime.strftime("%Y-%m-%d %H:%M:%S"): r.total_volume} for r in result]
    #     print(result_volume)
    #     template_data.append(result_volume)

    variables = {
        'data_sensors': template_data[:100]
    }

    print(template_data)
    return HttpResponse(template.render(variables,   request))


def trigger(request):
    print('d')


def results(request, result_id):
    template = loader.get_template(CHART)
    result_query = Measurement.objects.filter(sensor_object_id=result_id)
    print(result_id)
    print(result_query)
    data = {entry.datetime.strftime("%Y-%m-%d %H:%M:%S") : entry.total_volume if entry.total_volume is not None else 0 for entry in result_query}
    variables = {
        'data': data
    }
    return HttpResponse(template.render(variables, request))
