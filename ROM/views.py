from email import message
from logging.handlers import RotatingFileHandler
from multiprocessing import context
from django.db import IntegrityError
from django.http.response import JsonResponse
from unicodedata import category
from django.shortcuts import render,redirect
from django .http import HttpResponse, HttpResponseRedirect
from django .forms import inlineformset_factory
from rom_cleaning_services.settings import EMAIL_HOST_PASSWORD, EMAIL_HOST_USER
from .models import*
from .forms import OfferForm, OrderForm, CustomerForm,ServiceForm,PaymentForm,GiftForm
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from .filters import OrderFilter
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import FormView
from django.views.generic import TemplateView
from django.dispatch import receiver
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from paypal.standard.forms import PayPalPaymentsForm




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

   context = {
      'orders': orders, 
      'customers': customers, 
      'total_orders': total_orders, 
      'completed': completed, 
      'pending':pending, 
      'payment':payment, 
      'service':service, 
      'offers':offers, 
      'gifts':gifts }

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
   recipient_name = request.POST.get("recepient")
   recipient_email = request.POST.get("remail")
   subject = request.POST.get("subject")
   amount = request.POST.get("amount")


   gift_card = GiftCard.objects.create(
      name = f_name,
      email = email,
      recipient_name =  recipient_name,
      recipient_email =  recipient_email,
      phone_number = number,
      message = subject,
      giftcard_amount = amount
   )

   email_message = "Hello, you have areceived a giftcard from"+f_name

   gift = {
        'gift' : gift_card
    }
   text_body = email_message
   html_body = render_to_string('ROM/frontend/email_template.html', gift)

   mail = EmailMultiAlternatives(
      subject = subject,
      from_email =  "lindaatieno24@gmail.com",
      to = [recipient_email],
      body = text_body
   )
   mail.attach_alternative(html_body, 'text/html')
   mail.send()

   context = {
      "gift": gift_card
   }

   return render(request, 'ROM/frontend/checkout.html', context)         


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

   OrderFormSet = inlineformset_factory(Customer, Order, fields=('customer_id','service_category','status', 'total'), extra=5)

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
      return redirect('/gifts')

   context= {'item': gift}

   return render(request, 'ROM/admin/gift_delete.html', context)     



def getGiftCards(request) :

   return render(request, 'ROM/frontend/gift_card.html') 

def getQuoteForm(request) :

   services = Service.objects.all()

   context = {
      "services" : services
   }

   return render(request, 'ROM/frontend/quote_form.html', context)    

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
    fields = '__all__'
    template_name= "ROM/admin/order_details.html"


def orders(request):

   customers = Customer.objects.all()
   
   order = Order.objects.all()
  

   context = {
      'orders' : order,
      'customers':customers

      
   }


   return render(request, 'ROM/admin/order.html', context)        


@login_required
def orderDetail(request):
   success=False
   message = ""
   
   if request.method == "POST":
     
      f_name = request.POST.get("fullname")
      email = request.POST.get("email")
      number =request.POST.get("phone_number")
      address = request.POST.get("address")
      city = request.POST.get("city")
      state = request.POST.get("state")
      zip = request.POST.get("zip")
      about = request.POST.get("about")
      home= request.POST.get("home")
      bedroom= request.POST.get("bedroom")
      sqrft= request.POST.get("sqrft")
      bathroom= request.POST.get("bathrooms")
      floors= request.POST.get("floors")
      occupants= request.POST.get("occupants")
      space= request.POST.get("space")
      pets=request.POST.get("pets")
      npets=request.POST.get("npets")
      service= request.POST.get("service")
      frequency= request.POST.get("frequency")
      schedule= request.POST.get("schedule")
      subject = request.POST.get("subject")
      status = request.POST.get("status")

      total = findPriceByFeet(sqrft)

      if npets:
         npets = int(npets)
      else:
         npets = 0

      if 'No' in pets:
         pets = 1
      else: 
         pets = 0

      space = getSpaceDetails(request)
     
      customer = Customer.objects.filter(email= email).first()
      if customer is None:
         customer = Customer.objects.create(
               name = f_name,
               email = email,
         
         )

      print(service)
      service = Service.objects.filter(pk = service).first()

      order = Order.objects.create(
         customer_id = customer,
         service_category = service,
         phone_number = number,
         email= email,
         address =address,
         city = city,
         state = state,
         zip = zip,
         about = about,
         home= home,
         bedroom=bedroom,
         bathroom=bathroom,
         sqrft= sqrft,
         floors= floors,
         occupants= occupants,
         space= space,
         pets= pets,
         npets= npets,
         frequency= frequency,
         schedule= schedule,
         subject = subject,
         total = getFinalTotal(total, request),
         status = "pending"
      )

      # order = Order()
      # order.customer_id = customer
      # order.service_category = service,
      # order.phone_number = number,
      # order.email= email,
      # order.address =address,
      # order.city = city,
      # order.state = state,
      # order.zip = zip,
      # order.about = about,
      # order.home= home,
      # order.bedroom=bedroom,
      # order.bathroom=bathroom,
      # order.sqrft= sqrft,
      # order.floors= floors,
      # order.occupants= occupants,
      # order.space= space,
      # order.pets= pets,
      # order.npets= npets,
      # order.frequency= frequency,
      # order.schedule= schedule,
      # order.subject = subject
      

      # order.save()
  
      return HttpResponseRedirect("/order/checkout/"+str(order.id))

def checkoutOrder(request, id):
   
   try:
      order = Order.objects.select_related("customer_id").get(pk=id)
      context = {
         "order" : order
      }
      return render(request, 'ROM/frontend/checkout.html', context)

   except Order.DoesNotExist:

      return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def markAsComplete(request):

    order_id= request.POST.get("order_id")

    order = Order.objects.get(pk=order_id)
    order.status = "completed"
    order.save()

    data = {
        'success' : True
        }

    return JsonResponse(data)



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
      

   return price

 
def getSpaceDetails(request):
   space = ""

   if request.POST.get("office"):
      space = space + ", "+request.POST.get("office")
   if request.POST.get("basement"):
      space = space + ", "+request.POST.get("basement")
   if request.POST.get("play"):
      space = space + ", "+request.POST.get("play")
   if request.POST.get("family"):
      space = space + ", "+request.POST.get("family")
   if request.POST.get("dining"):
      space = space + ", "+request.POST.get("dining")

   return space


def getFinalTotal(total, request):

   if request.POST.get("oven"):
      total = total + int(request.POST.get("oven"))

   if request.POST.get("refrigerator"):
      total = total + int(request.POST.get("refrigerator"))

   if request.POST.get("patio"):
      total = total + int(request.POST.get("patio"))

   return total




# send email details
def sendMail(message, subject, email):

    context = {
        'message' : message
    }
    text_body = message
    html_body = render_to_string('ROM/frontend/email_template.html', context)

    mail = EmailMultiAlternatives(
        subject = subject,
        from_email =  settings.EMAIL_HOST_USER,
        to = ['lindaatieno24@gmail.com'],
        body = text_body
    )
    mail.attach_alternative(html_body, 'text/html')
    mail.send()
    
    

# class PaypalFormView(FormView):
#     template_name = 'paypal_form.html'
#     form_class = PayPalPaymentsForm

#     def get_initial(self):
#         return {
#             "business": 'bizlinda@gmail.com',
#             "amount": 20,
#             "currency_code": "USD",
#             "item_name": ' order_id',
#             "invoice": 1234,
#             "notify_url": self.request.build_absolute_uri(reverse('paypal-ipn')),
#             "return_url": self.request.build_absolute_uri(reverse('paypal-return')),
#             "cancel_return": self.request.build_absolute_uri(reverse('paypal-cancel')),
#             "lc": 'EN',
#             "no_shipping": '1',
#         }


# class PaypalReturnView(TemplateView):
#     template_name = 'paypal_success.html'

# class PaypalCancelView(TemplateView):
#     template_name = 'paypal_cancel.html'   



# @receiver(valid_ipn_received)
# def paypal_payment_received(sender, **kwargs):
#     ipn_obj = sender
#     if ipn_obj.payment_status == ST_PP_COMPLETED:
#         # WARNING !
#         # Check that the receiver email is the same we previously
#         # set on the `business` field. (The user could tamper with
#         # that fields on the payment form before it goes to PayPal)
#         if ipn_obj.receiver_email != 'bizlinda@gmail.com':
#             # Not a valid payment
#             return

#         # ALSO: for the same reason, you need to check the amount
#         # received, `custom` etc. are all what you expect or what
#         # is allowed.
#         try:
#             my_pk = ipn_obj.invoice
#             Payment = Payment.objects.get(pk=my_pk)
#             assert ipn_obj.mc_gross ==  Payment.amount and ipn_obj.mc_currency == 'USD'
#         except Exception:
#             logger.exception('Paypal ipn_obj data not valid!')
#         else:
#              Payment.paid = True
#              Payment.save()
#     else:
#         logger.debug('Paypal payment status not completed: %s' % ipn_obj.payment_status)         