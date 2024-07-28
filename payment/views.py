from django.shortcuts import render, redirect
from card.cart import Cart
from .models import ShippingAddress, Order, Order_item
from .forms import ShippingInfo, PaymentForm
from django.contrib import messages
from store.models import ProductSize
import smtplib
from payment.models import CuponCode
from payment.email_utils import send_order_confirmation
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
        'cupon_code': ''
    }

        #cehcking is prices is cahnged because of cupon code and updating new sum price at order summary
    if 'cupon' in request.session:
        context['summary'] = request.session['new_sum']
        context['cupon_code'] = request.session['cupon']
 


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
            'billing_form': billing_form,
            'cupon_code': ''
        }

        #cehcking is prices is cahnged because of cupon code and updating new sum price at order summary
        if 'cupon' in request.session:
            context['summary'] = request.session['new_sum']
            context['cupon_code'] = request.session['cupon']


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

    if request.session['pay_methode'] == 'at_address' or request.session['pay_methode'] == 'pay_to_account' :   

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

            shipping_address = f"{my_shipping['city']}\n{my_shipping['address']}\n{my_shipping['add_information']}\n{my_shipping['zipcode']}"

            set_order = Order(user=user, fullname=fullname, email=email, address=shipping_address, total_paid_amount=total_paid, phone=phone)
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
                        # for x in ProductSize.objects.all():
                        #     if x.product == product_item and x.size == size:
                        #         curent_qu = x.quantity
                        #         x.quantity = curent_qu - quantity
                        #         x.save()                               
                                
                                     
                                    

            # Send purchase confirmation email to the customer
            sum_order = []
            for key, item in quantities.items():
                for product in cart_products:
                    # name in email will be in georgian
                    if request.LANGUAGE_CODE == 'ka':
                        if product.name == item['name']:
                            sum_item = {
                                'em_name': product.name,
                                'em_price': product.new_price if product.sale > 0 else item['price'],
                                'em_size': item['size'],
                                'em_quantity': item['quantity']
                            }
                            sum_order.append(sum_item)
                    # name in email will be in english
                    elif request.LANGUAGE_CODE == 'en':
                        if product.name == item['name']:
                                sum_item = {
                                    'em_name': product.name_en,
                                    'em_price': product.new_price if product.sale > 0 else item['price'],
                                    'em_size': item['size'],
                                    'em_quantity': item['quantity']
                                }
                                sum_order.append(sum_item)            

            #changing totalpaid for email if therew is  a cuponcode
            if 'cupon' in request.session:
                total_paid =  request.session['new_sum']           

            EMAIL = env('MY_EMAIL')
            EXCAVATIOPASS = env('EMAIL_PASSWORD')
            content = {'order_num': f"Order number: {order.pk}",  'sum': total_paid, 'shipping_address':shipping_address}

            # Create the email message
            
            msg = send_order_confirmation(email, content, EMAIL, sum_order, language=request.LANGUAGE_CODE)
 
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

            


            #update payment mehtod in the order
            pay_method = request.session['pay_methode']
            order.payment_methode = pay_method
            order.save()


            # delet cupon code form db
            if 'cupon' in request.session:
                entered_code = request.session['cupon']
                codes_in_db = CuponCode.objects.filter(code=entered_code)

                if codes_in_db.exists():

                    order.total_paid_amount = request.session['new_sum']
                    order.cupon_used = f"{codes_in_db[0].sale_percentage}% code was used. code is:{codes_in_db[0].code}"
                    order.save()

                    #deleting cupon_code from database after successfull checkout
                    #for now we are not deleting it and alwo user to use it meny times
                    #codes_in_db[0].delete()
                
            # deleting session
            if 'cupon' in request.session:
                del request.session['cupon']
                del request.session['new_sum']

            messages.success(request, "Order Placed")
            # redirect to gome
            return redirect('home')
        else:
            messages.error(request, "Shipping information is missing.")
            return redirect('checkout')
    
    # after implementing card payment i should update this part 
    else:
        #if porchuse is not ok that regenerate item size quantity
        for x in ProductSize.objects.all():
            if x.product == product_item and x.size == size:
                curent_qu = x.quantity
                x.quantity = curent_qu + quantity
                x.save()                               
    
        return redirect('home')
    
