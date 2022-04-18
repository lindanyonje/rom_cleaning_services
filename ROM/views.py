from email import message
from logging.handlers import RotatingFileHandler
from multiprocessing import context
from django.db import IntegrityError
from django.http.response import JsonResponse
from unicodedata import category
from django.shortcuts import render,redirect
from django .http import HttpResponse, HttpResponseRedirect
from django .forms import inlineformset_factory
from .models import*
from .forms import OfferForm, OrderForm, CustomerForm,ServiceForm,PaymentForm,GiftForm
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from .filters import OrderFilter
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages



# Create your views here.


def home(request):

   reviews = Review.objects.filter(status = "approved")[:6]

   context = {
      'reviews' : reviews
   }

   return render(request, 'ROM/frontend/home.html', context)

@login_required
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


class CreateInquiry(LoginRequiredMixin, CreateView):
   model = Inquiry
   fields = '__all__'
   template_name = 'ROM/admin/inquiry.html'
   success_url = '/dashboard'


def get_cart(request):
    cart_items = Cart.objects.filter(order_id__isnull = True)
    
    return render(request, 'ROM/frontend/cart.html', {'cart': cart_items})    


def deleteCart(request):

    cart_id = request.POST.get('cart_id')
    cart_item= Cart.objects.get(pk = cart_id)
    cart_item.delete()
    

    data ={}

    return JsonResponse(data)

def checkoutDetails(request, total):

    context = {
            'total' : total,
        }
    return render(request, 'ROM/frontend/checkout.html', context)


def finalizeCheckout(request):
    if request.method == "GET":

        return render(request, 'shop/frontend/cart.html', context={})

    else:
        name=request.POST.get('name')
        email=request.POST.get('email')
        total=request.POST.get('total')
        order_number= "BURA_123_56"
        address=request.POST.get('address')
        delivery_method = request.POST.get("delivery_method")
        payment_mode = request.POST.get("paymentMode")
        
        customer = Customer.objects.filter(email= email).first()
        if customer is None:
            customer = Customer.objects.create(
                name = name,
                email = email,
                password = email,
            )
        order = Order.objects.create(
            total = total,
            order_number = order_number,
            status = "Pending",
            customer_id = customer

        )

        cart_items = Cart.objects.filter(order_id__isnull = True).update(order_id = order.id)

        context = {
            'order' : order.id,
        }

        return JsonResponse(context)

@login_required
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


def createGiftCard(request):

   f_name = request.POST.get("firstname")
   number = request.POST.get("phone_number")
   email = request.POST.get("email")
   subject = request.POST.get("subject")
   amount = request.POST.get("amount")

   GiftCard.objects.create(
      name = f_name,
      email = email,
      phone_number = number,
      message = subject,
      giftcard_amount = amount
   )

   context = {
      
   }

   return render(request, 'ROM/frontend/inquiry_success.html', context)         


@login_required
class CreateCustomer(LoginRequiredMixin,CreateView):
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

@login_required
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

 

@login_required
def deleteCustomer(request, pk):

   customer = Customer.objects.get(id=pk)

   if request.method == 'POST':
      customer.delete()
      return redirect('/customer')

   context= {'item': customer}

   return render(request, 'ROM/admin/customer_delete.html', context)         




class CreateService(LoginRequiredMixin, CreateView):
   model = Service
   fields = '__all__'
   template_name = 'ROM/admin/service_form.html'
   success_url = '/dashboard'

@login_required
def service(request):

   service = Service.objects.all()

   context={'service': service}

   return render(request, 'ROM/admin/service.html', context)


@login_required
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




@login_required
def deleteService(request, pk):

   service= Service.objects.get(id=pk)
   

   if request.method == 'POST':
      service.delete()
      return redirect('/service')

   context= {'item': service}

   return render(request, 'ROM/admin/service_delete.html', context)         





class CreateOrder(LoginRequiredMixin, CreateView):
   model = Order
   fields = '__all__'
   template_name = 'ROM/admin/order_form.html'
   success_url = '/dashboard'

@login_required
def getOrders(request):

   orders = Order.objects.all()

   return render(request, 'ROM/admin/order.html', {'orders': orders})

@login_required
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

@login_required
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


@login_required
def deleteOrder(request, pk):

   order= Order.objects.get(id=pk)

   if request.method == 'POST':
      order.delete()
      return redirect('/dashboard')

   context= {'item': order}

   return render(request, 'ROM/admin/order_delete.html', context)         

# def rating(request):

@login_required
def review(request):

   reviews= Review.objects.all()

   context = {
      'reviews' : reviews
   }


   return render(request, 'ROM/admin/review.html', context)  



def createReview(request):
   success=False
   message = ""
   
   if request.method == "POST":
      rating=request.POST.get("rating")
      f_name = request.POST.get("fullname")
      number = request.POST.get("phone_number")
      email = request.POST.get("email")
      subject = request.POST.get("subject")

      customer = Customer.objects.filter(email = email).first()

      if customer:
         
         try:
            
            Review.objects.create(
                  customer_id = customer,
                  rating = rating,
                  review= subject,

               )
            success=True
            message= "Thank you for your review"

            print(":::::CREATED MESSAGE::::::"+message)
         
         except IntegrityError as e:
            print("INTEGRITY ERROR: "+str(e))
            message = "INTEGRITY ERROR"+str(e)

   data = {
      "success":success,
      "message": message
   }

   return JsonResponse(data)    


@login_required      
def updateReviewStatus(request, pk):

   ##Using get can give a 404 error: Use try except
   review= Review.objects.get(id=pk)

   if "pending" in review.status:
      review.status = "approved"
   else:
      review.status = "pending"

   review.save()

   messages.success(request, 'Review updated successfully.')

   return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def deletereview(request, pk):

   review= Review.objects.get(id=pk)

   if request.method == 'POST':
      review.delete()
      return redirect('/review')

   context= {'item': review}

   return render(request, 'ROM/admin/review_delete.html', context)     


     


@login_required
def getPayment(request):
   payment= Payment.objects.all()

   return render(request, 'ROM/admin/payment.html', {'payment':payment})   

@login_required
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


@login_required
def deletePayment(request, pk):

   payment= Payment.objects.get(id=pk)

   if request.method == 'POST':
      payment.delete()
      return redirect('/payment')

   context= {'item': payment}

   return render(request, 'ROM/admin/payment_delete.html', context)     

@login_required
def getOfferList(request):
   offers= Offer.objects.all()

   return render(request, 'ROM/admin/offer_list.html', {'offers': offers})    



@login_required
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


@login_required
def deleteOffer(request, pk):

   offer= Offer.objects.get(id=pk)

   if request.method == 'POST':
      offer.delete()
      return redirect('/offers')

   context= {'item': offer}

   return render(request, 'ROM/admin/offer_delete.html', context)     


def getOffers(request):
   

   return render(request, 'ROM/frontend/offer.html')    

@login_required
def getGifts(request):
   gifts= GiftCard.objects.all()

   return render(request, 'ROM/admin/gifts.html', {'gifts':gifts}) 

@login_required
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


@login_required
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


class CustomerList(LoginRequiredMixin, ListView):

    login_required= True
    model = Customer
    template_name= "ROM/admin/customer_list.html"


class CustomerDetail(LoginRequiredMixin, DetailView):

    login_required= True
    model =  Customer
    template_name= "ROM/admin/customer_details.html"



@login_required
class OrderList(ListView):

    login_required= True
    model =Order
    template_name= "ROM/admin/order_list.html"

class OrderDetail(LoginRequiredMixin, DetailView):

    login_required= True
    model = Order
    template_name= "ROM/admin/order_details.html"


@login_required
def order(request):
   success=False
   message = ""
   
   if request.method == "POST":
     
      f_name = request.POST.get("fullname")
      email = request.POST.get("email")
      number = request.POST.get("phone_number")
      address = request.POST.get("address")
      city = request.POST.get("city")
      state = request.POST.get("state")
      zip = request.POST.get("zip")
      about = request.POST.get("about")
      home= request.POST.get("home")
      bedroom= request.POST.get("bedroom")
      sqrft= request.POST.get("sqrft")
      floors= request.POST.get("floors")
      occupants= request.POST.get("occupants")
      space= request.POST.get("space")
      pets= request.POST.get("pets")
      npets= request.POST.get("npets")
      service= request.POST.get("service")
      frequency= request.POST.get("frequency")
      schedule= request.POST.get("schedule")
      subject = request.POST.get("subject")
      payment= request.POST.get("payment-type")
      cardnumber= request.POST.get("cardnumber")
      cardname= request.POST.get("cardname")
      valid= request.POST.get("valid")
      ccv= request.POST.get("ccv")
      checkbox= request.POST.get("checkbox")
     
      customer = Customer.objects.filter(email= email).first()
      if customer is None:
         customer = Customer.objects.create(
               name = f_name,
               email = email,
               password = email,
         )

      service = Service.objects.filter(category = "regular").first()
      order = Order.objects.create(
         customer_id = customer,
         service_id = service,
         status = "pending",
         total = findPriceByFeet(sqrft)
      )

      Order.objects.create(
         order = order,
         email = email,
         number = number,
         address =address,
         city = city,
         state = state,
         zip = zip,
         about = about,
         home= home,
         bedroom=bedroom,
         sqrft= sqrft,
         floors= floors,
         occupants= occupants,
         space= space,
         pets= pets,
         npets= npets,
         service= service,
         frequency= frequency,
         schedule= schedule,
         subject = subject,
         payment= payment-type,
         card_number= cardnumber,
         card_name= cardname,
         valid= valid,
         ccv= ccv,
         checkbox= checkbox,
         
      )
  


      return render(request, 'ROM/admin/order_details.html')



def findPriceByFeet(feet):

   feet = int(feet)
   price = 0

   if feet > 1000:
      price = 150
   elif feet > 1000 and feet < 1500:
      price = 180
   elif feet > 1500 and feet < 2000:
      price = 210
   elif feet > 2000 and feet < 2500:
      price = 240
   elif feet > 2500 and feet < 3000:
      price = 270
   elif feet > 3000 and feet < 3500:
      price = 300
   elif feet > 3500 and feet < 4000:
      price = 330
   elif feet > 4000 and feet < 4500:
      price = 370
   elif feet > 4500 and feet < 5000:
      price = 400
   elif feet > 5000 and feet < 5500:
      price = 430
   elif feet > 5500 and feet < 6000:
      price = 470
   elif feet > 6000 and feet < 6500:
      price = 500
   elif feet > 6500 and feet < 7000:
      price = 530
   elif feet > 7000 and feet < 7500:
      price = 556
   elif feet > 7500 and feet < 8000:
      price = 573
   elif feet > 8000 and feet < 8500:
      price = 589
      

 
