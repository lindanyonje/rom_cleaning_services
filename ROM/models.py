from django.db import models


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
    customer_id=models.ForeignKey('customer',on_delete=models.CASCADE, blank=True,null=True)
    # image=models.FileField(upload_to='images')
    rating=models.IntegerField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

   

class Review(models.Model):
    rating= models.IntegerField(null=False, blank=False) 
    review=models.TextField( null=True, blank=True)
    customer_id=models.ForeignKey('customer',on_delete=models.CASCADE, blank=True,null=True)
    order_id= models.ForeignKey('order',on_delete=models.CASCADE,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True) 


class Order(models.Model):

    STATUS=(
        ('pending', 'pending'),
        ('on going', 'on going'),
        ('completed','completed'),
    )

    customer_id=models.ForeignKey('customer',on_delete=models.CASCADE,blank=True,null=True)
    service_id=models.ForeignKey('service',on_delete=models.CASCADE,blank=True,null=True)
    status=models.CharField(max_length=100, null=False, blank=False, choices=STATUS)
    total=models.FloatField(null= False, blank= True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_number



class GiftCard(models.Model):
    order_id= models.ForeignKey('order',on_delete=models.CASCADE,blank=True,null=True)  
    giftcard_amount=models.IntegerField(null=False, blank=False) 
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)     


class Payment(models.Model):
    order_id= models.ForeignKey('order',on_delete=models.CASCADE,blank=True,null=True)
    amount=models.FloatField(null= True, blank= True)
    description=models.TextField(null=True, blank=True)
    invoice_number=models.CharField(max_length=50, null=False, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.invoice_number  



