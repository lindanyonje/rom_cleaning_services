from django.urls import path
from . import views
from django.conf import settings

from django.conf.urls.static import static
from ROM.views import *


urlpatterns=[
    path('', views.home, name="home"),
    path('dashboard/',views.adminDashboard,name="dashboard"),
    path('service/',views.service, name="service")
]