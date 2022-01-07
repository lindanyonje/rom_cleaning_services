from django.urls import path
from . import views
from django.conf import settings

from django.conf.urls.static import static
from ROM.views import *


urlpatterns=[
    path('', views.home, name="home"),
    path('dashboard/', views.adminDashboard,name="dashboard"),
    path('service/', views.service, name="service"),
    path('customer/', views.customer, name="customer"),
    path('update_customer/<pk>/', views.updateCustomer, name="update_customer"),
    path('delete_customer/<pk>/', views.deleteCustomer, name="delete_customer"),
    path('orders/', views.getOrders, name="order_list"),
    path('create_order/<pk>', views.createOrder, name="order"),
    path('update_order/<pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<pk>/', views.deleteOrder, name="delete_order"),
    path('payment/',views.Payment, name= 'payment'),
    path('review/',views.review, name= 'review'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)