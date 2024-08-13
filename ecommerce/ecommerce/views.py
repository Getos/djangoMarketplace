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
    num_of_items = 0

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(
            user=request.user, completed=False)
        cartitems = cart.cartitems.all()
        num_of_items = cartitems.count()  # Assuming you want to show the count of items

    context = {"cart": cart, "items": cartitems, "num_of_items": num_of_items}
    return render(request, "cart.html", context)


def add_to_cart(request):
    data = json.loads(request.body)
    product_id = data["id"]
    # Default to 1 if quantity is not provided
    quantity = data.get("quantity", 1)

    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(
            user=request.user, completed=False)
        cartitem, created = CartItem.objects.get_or_create(
            cart=cart, product=product)

        # Update the quantity of the cart item
        cartitem.quantity += quantity
        cartitem.save()

        # Optionally, you can return the updated number of items in the cart
        num_items = cart.cartitems.count()

        return JsonResponse({"num_items": num_items}, status=200)
    else:
        return JsonResponse({"error": "User not authenticated"}, status=401)
