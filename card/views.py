from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .cart import Cart
from store.models import Product, ProductSize
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required



def cart_sum(request):
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
         

    context  = {
        'cart_products' : cart_products,
        'quantities' : quantities,
        'summary': sum(prices),
    }


    return render(request, 'cart_sum.html', context)



def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Product, id=product_id)
        user_quantity = int(request.POST.get('user_quantity'))
        product_size = request.POST.get('product_size')
        cart.add(product=product, size=product_size, quantity=user_quantity)
        cart_count = cart.__len__()
        response = JsonResponse({'count': cart_count})
        messages.success(request, (f'Product: {product.name} added to the cart'))
        return response




def edit(request, id, size):
    cart = Cart(request)
    products = cart.get_quantities()
    product_form_model = get_object_or_404(Product, id=id)
    size_count = ProductSize.objects.filter(product=product_form_model)
    cart_key = f"{id}_{size}"
    for x in products.keys():
        if products[x]['id']== id and products[x]['size'] == size :
            product = products[x]
     

    context = {
        'product': product,
        'product_from_model': product_form_model,
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
    cart_key = f"{id}_{size}"
    cart = Cart(request)
    cart.delete(cart_key=cart_key)
    return redirect('cart_sum')

        