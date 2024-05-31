from django.shortcuts import render, redirect
from card.cart import Cart
from .models import ShippingAddress, Order, Order_item
from .forms import ShippingInfo, PaymentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import ProductSize, Product
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import environ

env = environ.Env()
environ.Env.read_env()


def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_products()
    quantities = cart.get_quantities()
    prices = []
    
    # Determine if the user is authenticated
    if request.user.is_authenticated:
        user_shipping_info = ShippingAddress.objects.get(user=request.user)
        shippingInfo_form = ShippingInfo(instance=user_shipping_info)
    else:
        user_shipping_info = None
        shippingInfo_form = ShippingInfo()

    # Calculate total prices
    if quantities:
        for key, item in quantities.items():
            for product in cart_products:
                if product.name == item['name']:
                    if product.sale > 0:
                        prices.append(product.new_price * item['quantity'])
                    else:
                        prices.append(product.price * item['quantity'])

    if request.method == 'POST':
        shippingInfo_form = ShippingInfo(request.POST, instance=user_shipping_info)
        if shippingInfo_form.is_valid():
            shipping_info = shippingInfo_form.save(commit=False)
            if request.user.is_authenticated:
                shipping_info.user = request.user
            shipping_info.save()
            # Save the shipping info in the session for guests
            if not request.user.is_authenticated:
                request.session['shipping_info'] = shippingInfo_form.cleaned_data
            return render(request, 'billing.html')
    else:
        if not request.user.is_authenticated:
            shippingInfo_form = ShippingInfo()

    context = {
        'cart_products': cart_products,
        'quantities': quantities,
        'summary': sum(prices),
        'shipping_info': shippingInfo_form,
    }
    if cart_products:
        return render(request, 'ch_out.html', context)
    else:
        return redirect('home')




def billing(request):
    if request.method == 'POST':
        cart = Cart(request)
        billing_form = PaymentForm()
        cart_products = cart.get_products()
        quantities = cart.get_quantities()
        prices = []
        shippingInfo = request.POST
        info_list = [x for x in shippingInfo if x in ("fullname", "email", "address", "city", "phone", "zipcode", "per_id", "add_information") and len(x)>0]
        shipping_sum = {f'{x.capitalize()}': shippingInfo[x] for x in info_list}

        # Save shipping info in session for guest users
        request.session['my_shippInfo'] = shippingInfo

        if quantities:
            for key, item in quantities.items():
                for product in cart_products:
                    if product.name == item['name']:
                        if product.sale > 0:
                            prices.append(product.new_price * item['quantity'])
                        else:
                            prices.append(product.price * item['quantity'])
        context = {
            'cart_products': cart_products,
            'quantities': quantities,
            'summary': sum(prices),
            'shipping_sum': shipping_sum,
            'billing_form': billing_form
        }
        return render(request, 'billing.html', context)
    else:
        return redirect('home')



def payment_success(request):
    return render(request, 'payment_success.html')



def proc_order(request):
    cart = Cart(request)
    cart_products = cart.get_products()
    quantities = cart.get_quantities()
    prices = []

    if quantities:
        for key, item in quantities.items():
            for product in cart_products:
                if product.name == item['name']:
                    if product.sale > 0:
                        prices.append(product.new_price * item['quantity'])
                    else:
                        prices.append(product.price * item['quantity'])

    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        my_shipping = request.session.get('my_shippInfo', None)
        
        if request.user.is_authenticated:
            user = request.user
        else:
            user = None  # No user associated for guest checkout

        if my_shipping:
            fullname = my_shipping['fullname']
            email = my_shipping['email']
            total_paid = sum(prices)
            phone = my_shipping['phone']
            per_id = my_shipping['per_id']
            shipping_address = f"{my_shipping['city']}\n{my_shipping['address']}\n{my_shipping['add_information']}\n{my_shipping['zipcode']}"

            set_order = Order(user=user, fullname=fullname, email=email, address=shipping_address, total_paid_amount=total_paid, phone=phone, per_id=per_id)
            set_order.save()

            order_id = set_order.pk
            order = Order.objects.get(id=order_id)

            for key, value in quantities.items():
                for pr in cart_products:
                    if value['name'] == pr.name and value['id'] == pr.id:
                        product_item = pr
                        quantity = value['quantity']
                        size = value['size']
                        if pr.sale > 0:
                            product_price = pr.new_price
                        else:
                            product_price = pr.price

                        set_order_item = Order_item(order=order, product=product_item, user=user, quantity=quantity, price=product_price, size=size)
                        set_order_item.save()
                        #updating products database after successful purchase
                        for x in ProductSize.objects.all():
                            if x.product == product_item and x.size == size:
                                x.quantity = x.quantity - quantity
                                x.save()

            # Send purchase confirmation email to the customer
            sum_order = []
            for key, item in quantities.items():
                for product in cart_products:
                    if product.name == item['name']:
                        sum_item = {
                            'em_name': item['name'],
                            'em_price': product.new_price if product.sale > 0 else item['price'],
                            'em_size': item['size'],
                            'em_quantity': item['quantity']
                        }
                        sum_order.append(sum_item)

            EMAIL = env('EXCAVATIO')
            EXCAVATIOPASS = env('EXCAVATIOPASS')
            message_content = f"Here is your order:\n" + "\n".join([f"n{x['em_name']}\n Price: ₾ {x['em_price']} \n Size: {x['em_size']} \n Quantity: {x['em_quantity']}" for x in sum_order])
            content = {'order_num': f"Order number: {order.pk}", 'message': message_content, 'sum': total_paid, 'shipping_address':shipping_address}

            # Create the email message
            msg = MIMEMultipart()
            msg['From'] = formataddr(('Ecomge', EMAIL))
            msg['To'] = email
            msg['Subject'] = 'Your order confirmation'

            body = f"{content['order_num']}\n{content['message']}\nTotal Paid: {content['sum']}\nShipping address: {content['shipping_address']}"
            msg.attach(MIMEText(body, 'plain', 'utf-8'))

            # Send the email
            with smtplib.SMTP('smtp.gmail.com', 587) as mail:
                mail.ehlo()
                mail.starttls()
                mail.login(EMAIL, EXCAVATIOPASS)
                mail.send_message(msg)

            # Empty the cart
            for key in list(request.session.keys()):
                if key == 'session_key':
                    del request.session[key]

            messages.success(request, "Order Placed")
            return redirect('home')
        else:
            messages.error(request, "Shipping information is missing.")
            return redirect('checkout')
    else:
        return redirect('home')
    
