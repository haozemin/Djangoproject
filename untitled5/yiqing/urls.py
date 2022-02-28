from django.contrib import admin
from django.urls import path
from . import  views
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',views.get_first_page,name='get_fist_page')
]