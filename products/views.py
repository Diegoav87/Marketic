from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Order
from .forms import ProductForm, OrderForm, UpdateOrderForm
from django.contrib.auth import get_user_model
User = get_user_model()
from django.http import HttpResponse
from accounts.decorators import action_permission, user_list_permission, order_permission_customer, order_permission_provider
from .filters import OrderFilter, ProviderFilter

# Create your views here.
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

@login_required
def create_product(request):
    form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user

            if 'img' in request.FILES:
                product.img = request.FILES['img']

            product.save()
            return redirect('products:product_list')

    return render(request, 'products/product_form.html', {'form': form})

@login_required
def user_product_list(request, username):
    user = User.objects.get(username__iexact=username)
    products = Product.objects.filter(user=user)
    return render(request, 'products/user_product_list.html', {'user_products': products, 'product_user': user})

@login_required
@action_permission
def update_product(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    user = request.user

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            form.save()
            return redirect('products:user_products', username=user.username)

    return render(request, 'products/product_form.html', {'form': form})

@login_required
@action_permission
def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    user = request.user

    if request.method == 'POST':
        product.delete()
        return redirect('products:user_products', username=user.username)

    return render(request, 'products/confirm_delete.html', {'product': product})

@login_required
def create_order(request, pk):
    product = Product.objects.get(id=pk)
    form = OrderForm()

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.provider = product.user
            order.customer = request.user
            order.product = product
            order.save()
            return redirect('products:product_list')

    return render(request, 'products/confirm_order.html', {'product': product, 'form': form})

@login_required
@user_list_permission
def customer_order_list(request, username):
    user = User.objects.get(username__iexact=username)
    orders = user.purchase_orders.all()

    order_filter = OrderFilter(request.GET, queryset=orders)
    orders = order_filter.qs

    return render(request, 'products/customer_order_list.html', {'orders': orders, 'order_filter': order_filter})

@login_required
@user_list_permission
def provider_order_list(request, username):
    user = User.objects.get(username__iexact=username)
    orders = user.selling_orders.all()

    provider_filter = ProviderFilter(request.GET, queryset=orders)
    orders = provider_filter.qs

    return render(request, 'products/provider_order_list.html', {'orders': orders, 'provider_filter': provider_filter})

@login_required
@order_permission_provider
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = UpdateOrderForm(instance=order)
    user = request.user

    if request.method == 'POST':
        form = UpdateOrderForm(request.POST, instance=order)

        if form.is_valid():
            form.save()
            return redirect('products:provider_order_list', username=user.username)

    return render(request, 'products/update_order.html', {'form': form})

@login_required
@order_permission_customer
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    user = request.user

    if order.status == 'Pending':
        if request.method == 'POST':
            order.delete()
            return redirect('products:customer_order_list', username=user.username)
    else:
        return HttpResponse('Sorry this product has already been shipped.')

    return render(request, 'products/confirm_delete_order.html', {'order': order})