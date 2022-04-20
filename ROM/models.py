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

    CATEGORY=(
        ('regular', 'regular'),
        ('commercial', 'commercial'),
        ('personalized','personalized'),
    )

    Payment=(
        ('paypal', 'paypal'),
        ('credit or debit card', 'credit or debit card'),
        
    )
   
    customer_id=models.ForeignKey('Customer',on_delete=models.CASCADE,blank=True,null=True)
    service_category=models.CharField(max_length=100, null=False, blank=False,choices=CATEGORY, default='regular')
    email=models.CharField(max_length=100, null=True, blank=True)
    phone_number=models.IntegerField(null= True, blank= True)
    address=models.CharField(max_length=100,null=True, blank=True)
    city=models.CharField(max_length=100, null=True, blank=True)
    state=models.CharField(max_length=100, null=True, blank=True)
    zip=models.IntegerField(null= True, blank= True)
    about=models.CharField(max_length=100, null=True, blank=True)
    home=models.CharField(max_length=100, null=True, blank=True)
    bedroom=models.IntegerField(null= True, blank= True)
    sqrft=models.IntegerField(null= True, blank= True)
    floors=models.IntegerField(null= True, blank= True)
    occupants=models.IntegerField(null= True, blank= True)
    space=models.CharField(max_length=100, null=False, blank=False)
    no_pets=models.IntegerField(null= True, blank= True)
    npets=models.IntegerField(null= True, blank= True)
    frequency=models.CharField(max_length=100,null=True, blank=True)
    schedule=models.CharField(max_length=100, null=False, blank=False)
    subject=models.CharField(max_length=100, null=False, blank=False)
    Payment=models.CharField(max_length=100, null=False, blank=False,choices=Payment, default='Paypal')
    card_number=models.IntegerField(null= False, blank= True, default=1)
    card_name=models.CharField(max_length=100, null=True, blank=True)
    valid=models.IntegerField(null=True, blank=True)
    ccv=models.IntegerField(null=True, blank=True)
    status=models.CharField(max_length=100, null=False, blank=False, choices=STATUS)
    total=models.FloatField(null= True, blank= True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.status



class GiftCard(models.Model):
   
    giftcard_amount=models.IntegerField(null=False, blank=False) 
    name=models.CharField(max_length=100,  null=True, blank=True)
    recipient_name=models.CharField(max_length=100, null=True, blank=True)
    email=models.CharField(max_length=100, null=True, blank=True)
    recipient_email=models.CharField(max_length=100, null=True, blank=True)
    phone_number=models.IntegerField(null= True, blank= True)
    message=models.TextField(null=True, blank=True)
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

    # PaymentType=(
    #     ('paypal', 'paypal'),
    #     ('credit or debit card', 'credit or debit card'),
        
    # )
    # PaymentType=models.CharField(max_length=100, null=False, blank=False,choices=PaymentType, default='Paypal')
    customer_id= models.ForeignKey('Customer',on_delete=models.CASCADE,blank=True,null=True )
    order_id= models.ForeignKey('Order',on_delete=models.CASCADE,blank=True,null=True, related_name='+')
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

