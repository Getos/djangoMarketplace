from django.http import JsonResponse
from django.shortcuts import render
from products.models import Product
import json
from users.models import Cart, CartItem


def homepage(request):
    products = Product.objects.all()
    context = {
        'products': products}
    return render(request, 'index.html', context)


def cart(request):

    cart = None
    cartitems = []

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(
            user=request.user, completed=False)
        cartitems = cart.cartitems.all()

    context = {"cart": cart, "items": cartitems}
    return render(request, "cart.html", context)


def add_to_cart(request):
    data = json.loads(request.body)
    product_id = data["id"]
    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(
            user=request.user, completed=False)
        cartitem, created = CartItem.objects.get_or_create(
            cart=cart, product=product)
        cartitem.quantity += 1
        cartitem.save()

        num_of_item = cart.num_of_items

        print(cartitem)
    return JsonResponse(num_of_item, safe=False)
