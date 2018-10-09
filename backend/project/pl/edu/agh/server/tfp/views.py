from django.template import loader
from django.http import HttpResponse

from pl.edu.agh.server.tfp.util.templates import INDEX
from pl.edu.agh.server.tfp.task.data_fetcher import DownloadTask


def index(request):
    template = loader.get_template(INDEX)
    variables = {}
    return HttpResponse(template.render(variables, request))


def trigger(request):
    print('d')
    # DownloadTask().main()

