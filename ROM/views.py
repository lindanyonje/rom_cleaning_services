from django.shortcuts import render,redirect
from django .http import HttpResponse
from django .forms import inlineformset_factory
from .models import*
from .forms import OrderForm, CustomerForm
from django.views.generic import ListView
from django.views.generic.detail import DetailView
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


def customer(request):

   customers = Customer.objects.all()

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


def getOrders(request):

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


def getOfferList(request):

   return render(request, 'ROM/admin/offer_list.html')     

def getOffers(request):

   return render(request, 'ROM/frontend/offer.html')     


def getGifts(request):

   return render(request, 'ROM/admin/gifts.html') 

def getGiftCards(request) :

   return render(request, 'ROM/frontend/gift_card.html') 

def getQuoteForm(request) :

   return render(request, 'ROM/frontend/quote_form.html')    

def getService(request) :

   return render(request, 'ROM/frontend/service.html')   

def getQuote(request) :

   return render(request, 'ROM/frontend/quotte_form.html')       



class CustomerList(ListView):

    login_required= True
    model = Customer
    template_name= "ROM/admin/customer_list.html"


class CustomerDetail(DetailView):

    login_required= True
    model =  Customer
    template_name= "ROM/admin/customer_details.html"




# class OrderList(ListView):

#     login_required= True
#     model =Order
#     template_name= "ROM/admin/order_list.html"

class OrderDetail(DetailView):

    login_required= True
    model = Order
    template_name= "ROM/admin/order_details.html"