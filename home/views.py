from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    template = 'home/index.html'
    return HttpResponse(render(request, template))


def login_page(request):
    return HttpResponse("Still under development")
