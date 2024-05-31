from django.shortcuts import render, get_object_or_404
from .models import Product, Category, ProductSize
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils import translation
from django.http import HttpResponseRedirect
from django.conf import settings

def home(request):
    products = Product.objects.all()
    paginator = Paginator(products, 5)  # Show 5 products per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(request, 'home.html', context)


def details(request, pk):
    product = Product.objects.get(id=pk)
    size_count = ProductSize.objects.filter(product=product)
    max_quantity = int()
  


    context = {
        'product' : product,
        'size_count': size_count,
        'max_quantity': max_quantity

    }

    return render(request, 'details.html', context=context)




def category(request, cat_name):
    category = Category.objects.get(name=cat_name)
    products = Product.objects.filter(Category=category)
    paginator = Paginator(products, 5)  # Show 5 products per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'cat_name': cat_name
    }

    return render(request, 'categories.html', context)


def max_quantity(request):

    if request.POST.get('action') == 'post':
        product_size = request.POST.get('product_size')
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Product, id=product_id)
        sized_product = ProductSize.objects.filter(product=product)
        print('yes')

        for x in sized_product:
            if x.size == product_size:
                max_quantity = x.quantity
                
             

        response = JsonResponse({ 'max_quantity': max_quantity})
        return response




def quantity(request):
  if request.POST.get('action') == 'post':
        product_size = request.POST.get('product_size')
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Product, id=product_id)
        sized_product = ProductSize.objects.filter(product=product)

        for x in sized_product:
            if x.size == product_size:
                product_quantity = x.quantity

            

        response = JsonResponse({'size': product_size, 'product_quantity': product_quantity})
        return response


def set_language(request, lang_code):
    user_language = lang_code
    translation.activate(user_language)
    response = HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, user_language)
    return response