from django.shortcuts import render
from django.shortcuts import render
from products.models import Product


def homepage(request):
    products = Product.objects.all()
    context = {
        'products': products}
    return render(request, 'index.html', context)
