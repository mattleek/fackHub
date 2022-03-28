from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from . forms import UserRegisterForm
from django.utils.text import slugify
from django.shortcuts import render, redirect

from .models import Lender
from product.models import Product
from .forms import ProductForm


def become_lender(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            lender = Lender.objects.create(name=user.username, created_by=user)

            return redirect('frontpage')
    else:
        form = UserRegisterForm()

    return render(request, 'lender/become_lender.html', {'form': form})

@login_required
def lender_admin(request):
    lender = request.user.lender
    products = lender.products.all()
    orders = lender.orders.all() 
     
        
    for order in orders:
        order.lender_amount = 0
        order.lender_paid_amount = 0
        order.fully_paid = True

        for item in order.items.all():
            if item.lender == request.user.lender:
                if item.lender_paid:
                    order.lender_paid_amount += item.get_total_price()
                else:
                    order.lender_amount += item.get_total_price()
                    order.fully_paid = False

    return render(request, 'lender/lender_admin.html', {'lender': lender, 'products': products})


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.lender = request.user.lender
            product.slug = slugify(product.title)
            product.save()

            return redirect('lender_admin')
    else:
        form = ProductForm()
    
    return render(request, 'lender/add_product.html', {'form': form})