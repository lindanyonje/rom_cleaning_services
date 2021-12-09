from django.shortcuts import render,redirect
from django .http import HttpResponse
from django .forms import inlineformset_factory
from .models import*
from .forms import OrderForm
from django.views.generic.edit import CreateView
from .filters import OrderFilter

# Create your views here.


def home(request):

   return render(request, 'ROM/frontend/home.html')


def adminDashboard(request):

   orders= Order.objects.all()
   
   customers= Customer.objects.all()

   total_customers = customers.count()

   total_orders = orders.count()

   completed = orders.filter(status='Completed').count()

   pending = orders.filter(status='Pending').count()

   context = {'orders': orders, 'customers': customers, 'total_orders': total_orders, 
   'completed': completed, 'pending':pending }

    ##Declaring a dictionary used to package the data we shall
    ##send to the frontend html template for display.

   return render(request, 'ROM/admin/dashboard.html', context)


def customer(request, pk):

   customers = Customer.objects.get(id=pk)

   orders= Order.objects.all()
   total_orders = orders.count()
   myFilter= OrderFilter()

   # orders = Customer.order_set.all()

   context = {'customer':customers,'orders': orders,'total_orders': total_orders, 'myFilter': myFilter}

   return render(request, 'ROM/admin/customer.html', context)   


def service(request):

   service = Service.objects.all()

   return render(request, 'ROM/admin/service.html', {'service': service})

class CreateOrder(CreateView):
   model = Order
   fields = '__all__'
   template_name = 'ROM/admin/order_form.html'
   success_url = '/dashboard'


def createOrder(request, pk):

   customer = Customer.objects.get(id=pk)

   OrderFormSet = inlineformset_factory(Customer, Order, fields=('customer_id','service_id','status'), extra=5)

   formset= OrderFormSet(queryset=Order.objects.none(),instance=customer)
   # form= OrderForm(initial={'customer': customer})
   if request.method == 'POST':
      # print('POST:',request.POST)
      # form=OrderForm(request.POST)   
      formset= OrderFormSet(request.POST, instance=customer)
      if formset.is_valid():
         formset.save()
         return redirect('/dashboard')

   context= {'formset':formset}

   return render(request, 'ROM/admin/order_form.html', context)      


def updateOrder(request, pk):

   order= Order.objects.get(id=pk)
   form= OrderForm(instance=order)

   if request.method == 'POST':
  
      form=OrderForm(request.POST, instance=order)
      if form.is_valid():
         form.save()
         return redirect('/dashboard')

   context= {'form':form}

   return render(request, 'ROM/admin/order_form.html', context)         



def deleteOrder(request, pk):

   order= Order.objects.get(id=pk)

   if request.method == 'POST':
      order.delete()
      return redirect('/dashboard')

   context= {'item': order}

   return render(request, 'ROM/admin/delete.html', context)         



def review(request):

   return render(request, 'ROM/admin/review.html')      



def createPayment(request):

   return render(request, 'ROM/admin/payment.html')   




