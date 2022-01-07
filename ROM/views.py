from django.shortcuts import render,redirect
from django .http import HttpResponse
from django .forms import inlineformset_factory
from .models import*
from .forms import OrderForm, CustomerForm
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

   completed = orders.filter(status='completed').count()

   pending = orders.filter(status='pending').count()

   context = {'orders': orders, 'customers': customers, 'total_orders': total_orders, 
   'completed': completed, 'pending':pending }

    ##Declaring a dictionary used to package the data we shall
    ##send to the frontend html template for display.

   return render(request, 'ROM/admin/dashboard.html', context)


class CreateCustomer(CreateView):
   model = Customer
   fields = '__all__'
   template_name = 'ROM/admin/customer_form.html'
   success_url = '/dashboard'


def customer(request, pk):

   customers = Customer.objects.get(id=pk)

   orders= Order.objects.all()
   total_orders = orders.count()
   myFilter= OrderFilter(request.GET, queryset=orders)

   # orders = Customer.order_set.all()

   orders= myFilter.qs

   context = {'customers':customers,'orders': orders,'total_orders': total_orders, 'myFilter': myFilter}

   return render(request, 'ROM/admin/customer.html', context)   


def updateCustomer(request, pk):

   customer = Customer.objects.get(id=pk)
   form=CustomerForm(instance=customer)

   if request.method == 'POST':
  
      form=CustomerForm(request.POST, instance=customer)
      if form.is_valid():
         form.save()
         return redirect('/dashboard')

   context= {'form':form}

   return render(request, 'ROM/admin/customer_form.html', context)   


def deleteCustomer(request, pk):

   customer = Customer.objects.get(id=pk)

   if request.method == 'POST':
      customer.delete()
      return redirect('/dashboard')

   context= {'item': customer}

   return render(request, 'ROM/admin/delete.html', context)         





def service(request):

   service = Service.objects.all()

   return render(request, 'ROM/admin/service.html', {'service': service})

class CreateOrder(CreateView):
   model = Order
   fields = '__all__'
   template_name = 'ROM/admin/order_form.html'
   success_url = '/dashboard'


def order(request):

   order = Order.objects.all()

   return render(request, 'ROM/admin/order.html', {'order': order})


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

   orders= Order.objects.all()
   
   customers= Customer.objects.all()

   total_orders = orders.count()

   completed = orders.filter(status='Completed').count()

   context = {'orders': orders, 'customers': customers, 'total_orders': total_orders, 
   'completed': completed}


   return render(request, 'ROM/admin/review.html', context)      



def Payment(request):

   return render(request, 'ROM/admin/payment.html')   




