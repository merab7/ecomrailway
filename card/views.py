from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .cart import Cart
from store.models import Product, ProductSize
from django.http import JsonResponse
from payment.models import CuponCode
from django.views.decorators.http import require_http_methods


def cart_sum(request):
    cart = Cart(request)
    cart_products = cart.get_products()
    quantities = cart.get_quantities()
    prices = []
    new_sum = None

    if quantities:
        for key, item in quantities.items():
            for product in cart_products:
                if product.name == item['name']:
                    if product.sale > 0:
                        prices.append(product.new_price * item['quantity'])
                    else:
                        prices.append(product.price * item['quantity'])

    summary = sum(prices)

    # Retrieve coupon code and new_sum from session
    cupon_code = request.session.get('cupon')
    if cupon_code:
        coupon = CuponCode.objects.filter(code=cupon_code).first()
        if coupon:
            new_sum = summary - ((summary * coupon.sale_percentage) / 100)

    context = {
        'cart_products': cart_products,
        'quantities': quantities,
        'summary': new_sum if new_sum else summary,  # Use new_sum if coupon applied, otherwise regular summary
    }

    return render(request, 'cart_sum.html', context)



def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Product, id=product_id)
        user_quantity = int(request.POST.get('user_quantity'))
        product_size = request.POST.get('product_size')

        size_count = ProductSize.objects.filter(product=product)
        
        for item in size_count:
            if item.size == product_size:
                item.quantity = item.quantity - user_quantity
                item.save()



        if cart.contains(product=product, size=product_size):
            response = JsonResponse({'message': 'Product is already in the cart'})
            return response

        cart.add(product=product, size=product_size, quantity=user_quantity)
        cart_count = cart.__len__()
        response = JsonResponse({'count': cart_count})
        messages.success(request, f'Product: {product.name} added to the cart')
        return response

def is_in_cart(request):
    cart = Cart(request)
    product_id = int(request.POST.get('product_id'))
    product = get_object_or_404(Product, id=product_id)
    product_size = request.POST.get('product_size')
    
    in_cart = cart.contains(product=product, size=product_size)
    return JsonResponse({'in_cart': in_cart})



def edit(request, id, size):
    cart = Cart(request)
    products = cart.get_quantities()
    product_from_model = get_object_or_404(Product, id=id)
    size_count = ProductSize.objects.filter(product=product_from_model)
    cart_key = f"{id}_{size}"
    for x in products.keys():
        if products[x]['id']== id and products[x]['size'] == size :
            product = products[x]
     

    context = {
        'product': product,
        'product_from_model': product_from_model,
        'size_count': size_count,
        'cart_key': cart_key
    }
 
    return render(request, 'edit.html', context)



def update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Product, id=product_id)
        user_quantity = int(request.POST.get('user_quantity'))
        product_size = request.POST.get('product_size')
        cart_key = str(request.POST.get('cart_key'))
        cart.update(cart_key=cart_key, product=product, size=product_size, quantity=user_quantity)
        cart_count = cart.__len__()
        response = JsonResponse({'count': cart_count})
        
        return response
    

def cart_del(request, id , size):
    cart = Cart(request)

    
    
    #rebuild size quintity after deleting from cart
    product = get_object_or_404(Product, id=id)
    products_cart = cart.get_quantities()
    size_count = ProductSize.objects.filter(product=product)

    for x in products_cart.keys():
        if products_cart[x]['id']== id and products_cart[x]['size'] == size :
            user_quantity = products_cart[x]['quantity']

    for item in size_count:
        if item.size == size:
            item.quantity = item.quantity + user_quantity
            item.save()


  
    cart_key = f"{id}_{size}"
    cart.delete(cart_key=cart_key)

    # Check if cart is empty, then clear coupon code from session
    if cart.is_empty():
        if 'cupon' in request.session:
            del request.session['cupon']
        if 'new_sum' in request.session:
            del request.session['new_sum']

    return redirect('cart_sum')



def cupon_code(request):
    cart = Cart(request)
    cart_products = cart.get_products()
    quantities = cart.get_quantities()
    prices = [ ]     
    if quantities:
        for key, item in quantities.items():
             for product in cart_products:
                 if product.name == item['name']:
                     if product.sale > 0:
                          prices.append(product.new_price * item['quantity'])
                     else:
                         prices.append(product.price * item['quantity'])
    
    if request.POST.get('action') == 'post':  

        #add pay_method to a session
        pay_methode =  request.POST.get('pay_methode')
      


        entered_code = request.POST.get('cupon')
        codes_in_db = CuponCode.objects.filter(code=entered_code)

        if codes_in_db.exists():
            #adding cupon to a session for to after seccessful chekout delete it form db
            request.session['cupon'] = codes_in_db[0].code
            new_sum = sum(prices) - ((sum(prices) * codes_in_db[0].sale_percentage) / 100)
            print(new_sum)

            #adding new_sum for order summary section to the session
            request.session['new_sum'] = str(new_sum)

            response = JsonResponse({'new_sum': new_sum, 'percetage':codes_in_db[0].sale_percentage})

        else:
            response = JsonResponse({'error_text': 'Coupon code is not valid'}, status=400)

        return response


# add pay emthod to the session 
@require_http_methods(["GET"])
def pay_at_address(request):

    option = request.GET.get('shipping_option')
       # Handle the request data



    #adding payment method to the session
    request.session['pay_methode'] = option

    return JsonResponse({'status': 'success'})




        