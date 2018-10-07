from django.template import loader
from django.http import HttpResponse

from pl.edu.agh.server.tfp.util.templates import INDEX


def index(request):
    template = loader.get_template(INDEX)
    variables = {}
    return HttpResponse(template.render(variables, request))
