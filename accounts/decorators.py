from django.http import HttpResponse
from django.shortcuts import redirect
from products.models import Product, Order
from django.contrib.auth import get_user_model
User = get_user_model()

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def action_permission(view_func):
    def wrapper_func(request, *args, **kwargs):
        pk = kwargs.get('pk')
        product = Product.objects.get(id=pk)
        
        if product.user != request.user:
            return HttpResponse('You can not perform this action.')
        else:
            return view_func(request, *args, **kwargs)
    
    return wrapper_func

def user_list_permission(view_func):
    def wrapper_func(request, *args, **kwargs):
        username = kwargs.get('username')
        user = User.objects.get(username__iexact=username)
        
        if user != request.user:
            return HttpResponse('You can not perform this action.')
        else:
            return view_func(request, *args, **kwargs)
    
    return wrapper_func

def order_permission_provider(view_func):
    def wrapper_func(request, *args, **kwargs):
        pk = kwargs.get('pk')
        order = Order.objects.get(id=pk)
        
        if order.provider != request.user:
            return HttpResponse('You can not perform this action.')
        else:
            return view_func(request, *args, **kwargs)
    
    return wrapper_func

def order_permission_customer(view_func):
    def wrapper_func(request, *args, **kwargs):
        pk = kwargs.get('pk')
        order = Order.objects.get(id=pk)
        
        if order.customer != request.user:
            return HttpResponse('You can not perform this action.')
        else:
            return view_func(request, *args, **kwargs)
    
    return wrapper_func