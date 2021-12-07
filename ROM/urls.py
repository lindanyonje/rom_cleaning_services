from django.urls import path
from . import views
from django.conf import settings

from django.conf.urls.static import static
from ROM.views import *


urlpatterns=[
    path('', views.home, name="home"),
    path('dashboard/', views.adminDashboard,name="dashboard"),
    path('service/', views.service, name="service"),
    path('customer/<pk>/', views.customer, name="customer"),
    # path('create_order/', views.CreateOrder.as_view(), name="order"),
    path('create_order/<pk>', views.createOrder, name="order"),
    path('update_order/<pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<pk>/', views.deleteOrder, name="delete_order"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)