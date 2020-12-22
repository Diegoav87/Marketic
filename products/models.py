from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    description = models.TextField()
    img = models.ImageField(upload_to='images/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_LIST = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered')
    ]   

    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='selling_orders',  null=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchase_orders', null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=50, choices=STATUS_LIST, default='Pending')
    quantity = models.DecimalField(default=1, blank=True, max_digits=2, decimal_places=0)

    def __str__(self):
        return f'{self.product}: {self.customer}'

    def total(self):
        return self.product.price * self.quantity