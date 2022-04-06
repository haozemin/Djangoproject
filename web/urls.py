from django.contrib import admin
from django.urls import path,include
from web.views import  index

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', index.index,name='web_index'),#前台首页
]
