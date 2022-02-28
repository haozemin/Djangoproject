from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def get_first_page(request):
    return HttpResponse('hello world!')
