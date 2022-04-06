from django.shortcuts import render
from django.http import  HttpResponse
# 创建你的视图


def index(request):
    return  HttpResponse("欢迎进入前台的大堂")