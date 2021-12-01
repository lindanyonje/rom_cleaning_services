from django.shortcuts import render
from .models import*

# Create your views here.


def home(request):

   return render(request, 'ROM/frontend/home.html')


def adminDashboard(request):

    ##Declaring a dictionary used to package the data we shall
    ##send to the frontend html template for display.

   return render(request, 'ROM/admin/dashboard.html')


def customer(request):

   return render(request, 'ROM/admin/customer.html')   


def service(request):

   service = Service.objects.all()

   return render(request, 'ROM/admin/service.html', {'service': service})



def review(request):

   return render(request, 'ROM/admin/review.html')      


