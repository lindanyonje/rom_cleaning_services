from django.shortcuts import render
from .models import*

# Create your views here.


def home(request):

   return render(request, 'ROM/frontend/home.html')


def adminDashboard(request):

   orders= Order.objects.all()
   customers= Customer.objects.all()

   total_customers= customers.count()
   total_orders= orders.count()
   completed= orders.filter(status='Completed').count()
   pending= orders.filter(status='Pending').count()

   context={'orders': orders, 'customers': customers, 'total_orders': total_orders, 
   'completed': completed, 'pending':pending }

    ##Declaring a dictionary used to package the data we shall
    ##send to the frontend html template for display.

   return render(request, 'ROM/admin/dashboard.html', context)


def customer(request):

   return render(request, 'ROM/admin/customer.html')   


def service(request):

   service = Service.objects.all()

   return render(request, 'ROM/admin/service.html', {'service': service})



def review(request):

   return render(request, 'ROM/admin/review.html')      


