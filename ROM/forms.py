from django.forms import ModelForm

from .models import GiftCard, Order,Customer,Service,Payment,GiftCard, Offer, Inquiry


class OrderForm(ModelForm):
    class Meta:
        model= Order
        fields= ['customer_id', 'service_category', 'status', 'total']

class CustomerForm(ModelForm):
    class Meta:
        model= Customer
        fields= '__all__'

class ServiceForm(ModelForm):
    class Meta:
        model= Service
        fields= '__all__'        

class PaymentForm(ModelForm):
    class Meta:
        model= Payment
        fields= '__all__' 

class GiftForm(ModelForm):
    class Meta:
        model= GiftCard
        fields= '__all__' 


class OfferForm(ModelForm):
    class Meta:
        model= Offer
        fields= '__all__'

        
class InquiryForm(ModelForm):

    class Meta:
        model = Inquiry
        fields= '__all__'                                           