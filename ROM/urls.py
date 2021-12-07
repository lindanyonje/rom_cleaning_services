from django.urls import path
from . import views
from django.conf import settings

from django.conf.urls.static import static
from ROM.views import *


urlpatterns=[
    path('', views.home, name="home"),
    path('dashboard/',views.adminDashboard,name="dashboard"),
    path('service/',views.service, name="service"),
    path('customer/<str:id>/',views.customer, name="customer"),
    path('create_order/',views.createOrder, name="order"),
    path('update_order/<str:pk>/',views.updateOrder, name="update_order"),
]