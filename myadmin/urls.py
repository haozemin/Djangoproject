from django.contrib import admin
from django.urls import path,include
from myadmin.views import  index

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', index.index,name='myadmin_index'),#后台首页
]
