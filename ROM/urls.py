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
    path('customer/detail/<pk>',CustomerDetail.as_view(),name= 'Customer_detail'),
    path('update_customer/<pk>/', views.updateCustomer, name="update_customer"),
    path('delete_customer/<pk>/', views.deleteCustomer, name="delete_customer"),
    path('orders/', views.getOrders, name="order_list"),
    path('order/detail/<pk>', OrderDetail.as_view(),name= 'Order_detail'),
    path('create_order/<pk>', views.createOrder, name="order"),
    path('update_order/<pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<pk>/', views.deleteOrder, name="delete_order"),
    path('payment/',views.Payment, name= 'payment'),
    path('review/',views.review, name= 'review'),
    path('offer/',views.getOffers, name= 'offers'),
    path('offer_list/',views.getOfferList, name= 'offer_list'),
    path('gifts/',views.getGifts, name= 'gifts'),
    path('gift_card/',views.getGiftCards, name= 'gift_card'),
    path('quote_form/',views.getQuoteForm, name= 'quote'),
    path('services/',views.getService, name= 'services'),
    path('quotte_form/',views.getQuote, name= 'quotte'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)