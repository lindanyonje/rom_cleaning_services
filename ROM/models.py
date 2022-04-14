from wsgiref.validate import validator
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class Customer(models.Model):
    name=models.CharField(max_length=100, null=False, blank=False)
    email=models.CharField(max_length=100, null=False, blank=False)
    phone_number=models.IntegerField(null= True, blank= True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name



class Service(models.Model):

    CATEGORY=(
        ('regular', 'regular'),
        ('commercial', 'commercial'),
        ('personalized','personalized'),
    )
    
    category=models.CharField(max_length=100, null=False, blank=False,choices=CATEGORY, default='regular')
    description=models.TextField(null=False, blank=False)
    customer_id=models.ForeignKey('Customer',on_delete=models.CASCADE, blank=True,null=True)
    # image=models.FileField(upload_to='images')
    rating=models.IntegerField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category


class Inquiry(models.Model):
    name=models.CharField(max_length=100, null=False, blank=False)
    email=models.CharField(max_length=100, null=False, blank=False)
    phone_number=models.IntegerField(null= True, blank= True)
    message=models.TextField(null=False, blank=False)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Rating(models.Model):
    score= models.IntegerField(default=0, 
       validators=[
           MaxValueValidator (5),
           MinValueValidator (0),
       ]
    ) 
    def __str__(self):
      return str(self.pk)


class Review(models.Model):

    STATUS=(
        ('pending', 'pending'),
        ('approved', 'approved'),
    )
    rating= models.IntegerField(null=False, blank=False) 
    review=models.TextField( null=True, blank=True)
    customer_id=models.ForeignKey('Customer',on_delete=models.CASCADE, blank=True,null=True)
    status=models.CharField(max_length=100, default="pending", choices=STATUS)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    def getRatingRange(self):

        return range(self.rating) 


class Order(models.Model):

    STATUS=(
        ('pending', 'pending'),
        ('on going', 'on going'),
        ('completed','completed'),
    )

    customer_id=models.ForeignKey('Customer',on_delete=models.CASCADE,blank=True,null=True)
    service_id=models.ForeignKey('Service',on_delete=models.CASCADE,blank=True,null=True)
    status=models.CharField(max_length=100, null=False, blank=False, choices=STATUS)
    total=models.FloatField(null= False, blank= True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.status



class GiftCard(models.Model):
   
    giftcard_amount=models.IntegerField(null=False, blank=False) 
    name=models.CharField(max_length=100, null=False, blank=False,default="Some String")
    recipient_name=models.CharField(max_length=100, null=True, blank=True)
    email=models.CharField(max_length=100, null=False, blank=False, default="Some String")
    recipient_email=models.CharField(max_length=100, null=True, blank=True)
    phone_number=models.IntegerField(null= True, blank= True)
    message=models.TextField(null=False, blank=False, default="Some String")
    code=models.CharField(max_length=50, null=False, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)     


class Offer(models.Model):
    service_id= models.ForeignKey('Service',on_delete=models.CASCADE,blank=True,null=True)  
    offer_amount=models.IntegerField(null=False, blank=False) 
    code=models.CharField(max_length=50, null=False, blank=True)
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)     


class Payment(models.Model):
    customer_id= models.ForeignKey('Customer',on_delete=models.CASCADE,blank=True,null=True)
    order_id= models.ForeignKey('Order',on_delete=models.CASCADE,blank=True,null=True)
    amount=models.FloatField(null= True, blank= True)
    description=models.TextField(null=True, blank=True)
    invoice_number=models.CharField(max_length=50, null=False, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.invoice_number  



class Quote(models.Model):
    customer_id=models.ForeignKey('Customer',on_delete=models.CASCADE, blank=True,null=True)
    service_id= models.ForeignKey('Service',on_delete=models.CASCADE,blank=True,null=True)  
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)     



class Cart(models.Model):
    order_id= models.ForeignKey('order',on_delete=models.CASCADE,blank=True,null=True, related_name='carts')
    service_id=models.ForeignKey('service',on_delete=models.CASCADE,blank=True,null=True)
    quantity=models.IntegerField(null= False, blank= False) 
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now_add=True) 

class Checkout(models.Model):
     customer = models.ForeignKey('customer', on_delete=models.CASCADE)
     phonenumber = models.CharField(max_length=20, null=False)
     total = models.FloatField(default=0)
     amount_paid = models.FloatField(default=0, )
     address = models.CharField(max_length=300, null=True, blank=True)
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
     
     CHECKOUT_STATUS = (
         ('PENDING', 'Pending'),
         ('PAID', 'Paid'),
     )
     status = models.CharField(choices=CHECKOUT_STATUS, max_length=100, default='PENDING')


class OrderDetails(models.Model):
    order= models.ForeignKey('Order',on_delete=models.CASCADE,blank=True,null=True)
    email=models.CharField(max_length=100, null=False, blank=False)
    phone_number=models.IntegerField(null= True, blank= True)
    address=models.CharField(max_length=100, null=False, blank=False)
    city=models.CharField(max_length=100, null=False, blank=False)
    state=models.CharField(max_length=100, null=False, blank=False)
    zip=models.CharField(max_length=100, null=False, blank=False)
    about=models.CharField(max_length=100, null=False, blank=False)
    home=models.CharField(max_length=100, null=False, blank=False)
    bedroom=models.CharField(max_length=100, null=False, blank=False)
    sqrft=models.CharField(max_length=100, null=False, blank=False)
    floors=models.IntegerField(null= True, blank= True)
    occupants=models.IntegerField(null= True, blank= True)
    space=models.CharField(max_length=100, null=False, blank=False)
    no_pets=models.IntegerField(null= True, blank= True)
    npets=models.IntegerField(null= True, blank= True)
    frequency=models.CharField(max_length=100, null=False, blank=False)
    schedule=models.CharField(max_length=100, null=False, blank=False)
    subject=models.CharField(max_length=100, null=False, blank=False)
    payment=models.CharField(max_length=100, null=False, blank=False)
    card_number=models.IntegerField(null= True, blank= True)
    card_name=models.CharField(max_length=100, null=False, blank=False)
    valid=models.IntegerField(null= True, blank= True)



  



#  f_name = request.POST.get("fullname")
#       email = request.POST.get("email")
#       number = request.POST.get("phone_number")
#       address = request.POST.get("address")
#       city = request.POST.get("city")
#       state = request.POST.get("state")
#       zip = request.POST.get("zip")
#       about = request.POST.get("about")
#       home= request.POST.get("home")
#       bedroom= request.POST.get("bedroom")
#       sqrft= request.POST.get("sqrft")
#       floors= request.POST.get("floors")
#       occupants= request.POST.get("occupants")
#       space= request.POST.get("space")
#       no_pets= request.POST.get("pets")
#       npets= request.POST.get("npets")
#       service= request.POST.get("service")
#       frequency= request.POST.get("frequency")
#       schedule= request.POST.get("schedule")
#       subject = request.POST.get("subject")
#       payment= request.POST.get("payment-type")
#       card_number= request.POST.get("cardnumber")
#       card_name= request.POST.get("cardname")
#       valid= request.POST.get("valid")
#       ccv= request.POST.get("ccv")
#       