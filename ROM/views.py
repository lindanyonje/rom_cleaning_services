from email import message
from logging.handlers import RotatingFileHandler
from multiprocessing import context
from unicodedata import category
from django.shortcuts import render,redirect
from django .http import HttpResponse
from django .forms import inlineformset_factory
from .models import*
from .forms import OfferForm, OrderForm, CustomerForm,ServiceForm,PaymentForm,GiftForm
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from .filters import OrderFilter

# Create your views here.


def home(request):

   reviews = Review.objects.all()[:6]

   context = {
      'reviews' : reviews
   }

   return render(request, 'ROM/frontend/home.html', context)


def adminDashboard(request):

   orders= Order.objects.all()
   
   customers= Customer.objects.all()

   total_customers = customers.count()

   payment = Payment.objects.all()

   service= Service.objects.all()

   offers= Offer.objects.all()

   gifts= GiftCard.objects.all()

   total_orders = orders.count()

   completed = orders.filter(status='completed').count()

   pending = orders.filter(status='pending').count()

   context = {'orders': orders, 'customers': customers, 'total_orders': total_orders, 
   'completed': completed, 'pending':pending, 'payment':payment, 'service':service, 'offers':offers, 'gifts':gifts }

    ##Declaring a dictionary used to package the data we shall
    ##send to the frontend html template for display.

   return render(request, 'ROM/admin/dashboard.html', context)


class CreateInquiry(CreateView):
   model = Inquiry
   fields = '__all__'
   template_name = 'ROM/admin/inquiry.html'
   success_url = '/dashboard'


def inquiry(request):
   
   inquiry = Inquiry.objects.all()
  

   context = {
      'inquiries' : inquiry
   }


   return render(request, 'ROM/admin/inquiry.html', context)        



def createInquiry(request):

   f_name = request.POST.get("firstname")
   number = request.POST.get("phone_number")
   email = request.POST.get("email")
   subject = request.POST.get("subject")

   Inquiry.objects.create(
      name = f_name,
      email = email,
      phone_number = number,
      message = subject
   )

   context = {
      
   }

   return render(request, 'ROM/frontend/inquiry_success.html', context)      



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
         return redirect('/customer')

   context= {'form':form}

   return render(request, 'ROM/admin/customer_form.html', context)   

 


def deleteCustomer(request, pk):

   customer = Customer.objects.get(id=pk)

   if request.method == 'POST':
      customer.delete()
      return redirect('/customer')

   context= {'item': customer}

   return render(request, 'ROM/admin/customer_delete.html', context)         




class CreateService(CreateView):
   model = Service
   fields = '__all__'
   template_name = 'ROM/admin/service_form.html'
   success_url = '/dashboard'


def service(request):

   service = Service.objects.all()

   context={'service': service}

   return render(request, 'ROM/admin/service.html', context)



def updateService(request, pk):

   service = Service.objects.get(id=pk)
   form=ServiceForm(instance=service)

   if request.method == 'POST':
  
      form=ServiceForm(request.POST, instance=service)
      if form.is_valid():
         form.save()
         return redirect('/service')

   context= {'form':form}

   return render(request, 'ROM/admin/service_form.html', context)   





def deleteService(request, pk):

   service= Service.objects.get(id=pk)
   

   if request.method == 'POST':
      service.delete()
      return redirect('/service')

   context= {'item': service}

   return render(request, 'ROM/admin/service_delete.html', context)         





class CreateOrder(CreateView):
   model = Order
   fields = '__all__'
   template_name = 'ROM/admin/order_form.html'
   success_url = '/dashboard'


def getOrders(request):

   orders = Order.objects.all()

   return render(request, 'ROM/admin/order.html', {'orders': orders})


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

   return render(request, 'ROM/admin/order_delete.html', context)         

# def rating(request):


def review(request):

   reviews= Review.objects.all()

   context = {
      'reviews' : reviews
   }


   return render(request, 'ROM/admin/review.html', context)  


def createReview(request):

   rating=request.POST.get("rating")
   f_name = request.POST.get("fullname")
   number = request.POST.get("phone_number")
   email = request.POST.get("email")
   subject = request.POST.get("subject")

   customer = Customer.objects.filter(email = email).first()

   if customer:

      Review.objects.create(

         customer_id = customer,
         rating = rating,
         review= subject,

      )

   context = {
      
   }

   return render(request, 'ROM/frontend/review_success.html', context)          


def deletereview(request, pk):

   review= Review.objects.get(id=pk)

   if request.method == 'POST':
      review.delete()
      return redirect('/review')

   context= {'item': review}

   return render(request, 'ROM/admin/review_delete.html', context)     


     



def getPayment(request):
   payment= Payment.objects.all()

   return render(request, 'ROM/admin/payment.html', {'payment':payment})   


def updatePayment(request, pk):

   payment= Payment.objects.get(id=pk)
   form= PaymentForm(instance=payment)

   if request.method == 'POST':
  
      form=OrderForm(request.POST, instance=payment)
      if form.is_valid():
         form.save()
         return redirect('/payment')

   context= {'form':form}

   return render(request, 'ROM/admin/payment_form.html', context)         



def deletePayment(request, pk):

   payment= Payment.objects.get(id=pk)

   if request.method == 'POST':
      payment.delete()
      return redirect('/payment')

   context= {'item': payment}

   return render(request, 'ROM/admin/payment_delete.html', context)     


def getOfferList(request):
   offers= Offer.objects.all()

   return render(request, 'ROM/admin/offer_list.html', {'offers': offers})    




def updateOffer(request, pk):

   offer= Offer.objects.get(id=pk)
   form= OfferForm(instance=offer)

   if request.method == 'POST':
  
      form=OfferForm(request.POST, instance=offer)
      if form.is_valid():
         form.save()
         return redirect('/offers')

   context= {'form':form}

   return render(request, 'ROM/admin/offer_form.html', context)         



def deleteOffer(request, pk):

   offer= Offer.objects.get(id=pk)

   if request.method == 'POST':
      offer.delete()
      return redirect('/offers')

   context= {'item': offer}

   return render(request, 'ROM/admin/offer_delete.html', context)     


def getOffers(request):
   

   return render(request, 'ROM/frontend/offer.html')    


def getGifts(request):
   gifts= GiftCard.objects.all()

   return render(request, 'ROM/admin/gifts.html', {'gifts':gifts}) 


def updateGift(request, pk):

   gift= GiftCard.objects.get(id=pk)
   form= GiftForm(instance=gift)

   if request.method == 'POST':
  
      form=OrderForm(request.POST, instance=gift)
      if form.is_valid():
         form.save()
         return redirect('/gift')

   context= {'form':form}

   return render(request, 'ROM/admin/gift_form.html', context)         



def deleteGift(request, pk):

   gift= GiftCard.objects.get(id=pk)

   if request.method == 'POST':
      gift.delete()
      return redirect('/gift')

   context= {'item': gift}

   return render(request, 'ROM/admin/gift_delete.html', context)     



def getGiftCards(request) :

   return render(request, 'ROM/frontend/gift_card.html') 

def getQuoteForm(request) :

   return render(request, 'ROM/frontend/quote_form.html')    

def getService(request) :

   return render(request, 'ROM/frontend/myservices.html')   

def getQuote(request) :

   return render(request, 'ROM/frontend/quotte_form.html')   

def getOurStory(request):

   return render(request, 'ROM/frontend/Our_story.html')  


def getFaq(request):

   return render(request, 'ROM/frontend/FAQ.html')    


def getTos(request):

   return render(request, 'ROM/frontend/terms_of_service.html')        


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