import django_filters

from .models import Product, Order

class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = ('provider', 'product', 'status')

class ProviderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = ('customer', 'product', 'status')