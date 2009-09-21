from django.http import HttpResponse
from extdirect import DirectRouter
from registry import register_router

class DjangoDirectRouter(DirectRouter):
    def __call__(self, request):
        body = request.raw_post_data
        result = super(DjangoDirectRouter, self).__call__(body)
        return HttpResponse(result)
