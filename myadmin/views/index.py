from django.shortcuts import render
from django.http import  HttpResponse
# 创建你的视图


def index(request):
    # return  HttpResponse("欢迎进入点餐系统的后台管理")
    return render(request,'myadmin/index/admin.html')