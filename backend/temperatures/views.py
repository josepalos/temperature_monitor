from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.views.decorators.http import require_http_methods


@require_http_methods(["POST"])
@csrf_exempt
def receive_temperatures(request):
    data = bytearray(request.POST.get("data"), encoding='utf-8')
    temperatures = (int(d) for d in data)
    print(temperatures)

    return HttpResponse()
