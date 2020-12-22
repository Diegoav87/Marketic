from django import forms
from .models import Product, Order

class ProductForm(forms.ModelForm):
    class Meta:
        fields = ('name', 'description', 'img', 'price')
        model = Product
class OrderForm(forms.ModelForm):
    class Meta:
        fields = ('quantity', 'status')
        model = Order

class UpdateOrderForm(forms.ModelForm):
    class Meta:
        fields = ('status',)
        model = Order
