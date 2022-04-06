from django.contrib import admin
from django.urls import path,include
from mobile.views import  index

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', index.index,name='mobile_index'),#移动端首页
]
