from django.urls import path
from . import views
from django.conf import settings

from django.conf.urls.static import static
from ROM.views import *


urlpatterns=[
    path('', views.home, name="home"),
    path('dashboard/', views.adminDashboard,name="dashboard"),

    path('service/', views.service, name="service"),
    path('update_service/<pk>/', views.updateService, name="update_service"),
    path('delete_service/<pk>/', views.deleteService, name="delete_service"),

    path('customer/', views.customer, name="customer"),
    path('customer/detail/<pk>',CustomerDetail.as_view(),name= 'Customer_detail'),
    path('update_customer/<pk>/', views.updateCustomer, name="update_customer"),
    path('delete_customer/<pk>/', views.deleteCustomer, name="delete_customer"),

  
    path('orders/', views.getOrders, name="order_list"),
    path('order/detail/<pk>', OrderDetail.as_view(),name="Order_detail"),
    path('order/checkout/<id>', views.checkoutOrder,name="checkout.order"),
    path('create_order/', views.orderDetail, name="order"),
    path('update_order/<pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<pk>/', views.deleteOrder, name="delete_order"),
     path('order/mark/completed', views.markAsComplete, name="mark_as_complete"),



    path('payment/',views.getPayment, name= 'payment'),
    path('update_payment/<pk>/', views.updatePayment, name="update_payment"),
    path('delete_payment/<pk>/', views.deletePayment, name="delete_payment"),



    path('review/',views.review, name= 'review'),
    path('delete_review/<pk>/', views.deletereview, name="delete_review"),
    path('create/review/',views.createReview, name= "create.review"),
    path('update/review/<pk>/',views.updateReviewStatus, name= "update_review"),

    path('messages/',views.inquiry, name= 'inquiry'),
    path('create/inquiry/',views.createInquiry, name= 'create.inquiry'),


    path('offer/',views.getOffers, name= 'offers'),
    path('update_offer/<pk>/', views.updateOffer, name="update_offer"),
    path('delete_offer/<pk>/', views.deleteOffer, name="delete_offer"),
    path('offer_list/',views.getOfferList, name= 'offer_list'),
    

    path('gifts/',views.getGifts, name= 'gifts'),
    path('update_gift/<pk>/', views.updateGift, name="update_gift"),
    path('delete_gift/<pk>/', views.deleteGift, name="delete_gift"),
    path('create/GiftCard/',views.createGiftCard, name= 'create.gift'),

    path('gift_card/',views.getGiftCards, name= 'gift_card'),

    path('quote_form/',views.getQuoteForm, name= 'quote'),
    path('quotte_form/',views.getQuote, name= 'quotte'),

    path('services/',views.getService, name= 'services'),

   
    path('story/',views.getOurStory, name= 'story'),
    
    path('FAQ/',views.getFaq, name= 'FAQ'),
    path('TOS/',views.getTos, name= 'TOS'),

    path('end_email/', views.sendanemail, name="send_email"),


    path('/paypal-return/', views.PaypalReturnView.as_view(), name='paypal-return'),
    path('/paypal-cancel/', views.PaypalCancelView.as_view(), name='paypal-cancel'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)