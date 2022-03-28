from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from cart.cart import Cart

from .models import Order, OrderItem

def checkout(request, first_name, last_name, email, address, zipcode, place, phone, amount):
    order = Order.objects.create(first_name=first_name, last_name=last_name, email=email, address=address, zipcode=zipcode, place=place, phone=phone, paid_amount=amount)

    for item in Cart(request):
        OrderItem.objects.create(order=order, product=item['product'], lender=item['product'].vendor, price=item['product'].price, quantity=item['quantity'])
    
        order.lenders.add(item['product'].lender)

    return order

def notify_lender(order):
    from_email = settings.DEFAULT_EMAIL_FROM

    for lender in order.vendors.all():
        to_email = lender.created_by.email
        subject = 'New order'
        text_content = 'You have a new order!'
        html_content = render_to_string('order/email_notify_vendor.html', {'order': order, 'lender': lender})

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

def notify_customer(order):
    from_email = settings.DEFAULT_EMAIL_FROM

    to_email = order.email
    subject = 'Order confirmation'
    text_content = 'Thank you for the order!'
    html_content = render_to_string('order/email_notify_customer.html', {'order': order})

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()