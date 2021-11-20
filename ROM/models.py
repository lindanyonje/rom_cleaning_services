from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(User):
    phone_number=models.IntegerField(null= True, blank= True)
    
    def __str__(self):
        return self.name


class CustomerAddress(User):
    customer_id=models.ForeignKey('Customer',on_delete=models.CASCADE,blank=True,null=True)
    address=models.TextField(null=False, blank=False)
    pin=models.CharField(max_length=100, null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)



class Service(models.Model):
    name=models.CharField(max_length=100, null=False, blank=False)
    description=models.TextField(null=False, blank=False)
    image=models.FileField(upload_to='images')
    rating=models.IntegerField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    rating= models.IntegerField(null=False, blank=False) 
    review=models.TextField( null=True, blank=True)
    customer_id=models.ForeignKey('customer',on_delete=models.CASCADE,blank=True,null=True)
    service_id=models.ForeignKey('service',on_delete=models.CASCADE,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now_add=True) 


class Order(models.Model):
    total=models.IntegerField(null= False, blank= True)
    status=models.CharField(max_length=100, null=False, blank=False, default="Pending")
    order_number=models.CharField(max_length=100, null=False, blank=False)
    customer_id=models.ForeignKey('customer',on_delete=models.CASCADE,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_number



class GiftCard(models.Model):
    service_id= models.ForeignKey('service',on_delete=models.CASCADE,blank=True,null=True)  
    giftcard_amount=models.IntegerField(null=False, blank=False) 
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now_add=True)     


class Payment(models.Model):
    order_id= models.ForeignKey('order',on_delete=models.CASCADE,blank=True,null=True)
    amount=models.IntegerField(null= True, blank= True)
    description=models.TextField(null=True, blank=True)
    invoice_number=models.CharField(max_length=50, null=False, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.invoice_number  



