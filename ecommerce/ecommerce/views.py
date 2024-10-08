
from django.http import JsonResponse
from django.shortcuts import redirect, render
from products.models import Product
import json
from users.models import Cart, CartItem, Orders
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from users.models import CartItem
from django.db import transaction
from django.shortcuts import render
from ecommerce.utils.decorators import group_required


def homepage(request):
    products = Product.objects.all()
    num_of_items = cartcount(request)  # Get the count of items in the cart
    context = {
        'products': products,
        'num_of_items': num_of_items  # Pass num_of_items to the template
    }
    return render(request, 'index.html', context)


def cartcount(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(
            user=request.user, completed=False)
        num_of_items = cart.cartitems.count()
    else:
        num_of_items = 0  # Ensure that num_of_items is 0 for unauthenticated users
    return num_of_items


def cart(request):
    cart = None
    cartitems = []
    insufficient_stock_items = []
    # Use cartcount to get the number of items
    num_of_items = cartcount(request)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(
            user=request.user, completed=False)
        cartitems = cart.cartitems.all()

        # Check for items with insufficient stock
        for item in cartitems:
            if item.quantity > item.product.quantity:
                insufficient_stock_items.append(item.product.id)

    context = {
        "cart": cart,
        "items": cartitems,
        "num_of_items": num_of_items,
        "insufficient_stock_items": insufficient_stock_items  # Pass this to template
    }
    return render(request, "cart.html", context)


def add_to_cart(request):
    data = json.loads(request.body)
    product_id = data["id"]
# Default to 1 if quantity is not provided
    quantity = data.get("quantity", 1)

# Retrieve the product using the product_id
    try:
        product = Product.objects.get(id=product_id)
        available_quantity = product.quantity

        # Compare the cart quantity with the available quantity
        if quantity > available_quantity:
            messages.success(
                request, "quantity value quality is higher than avilable")
            return JsonResponse({"error": "quantity is not available"}, status=401)
        else:
            # Proceed with adding to cart
            print("Quantity is available, proceeding with cart update.")
            # Add to cart logic here...

    except Product.DoesNotExist:
        return JsonResponse({"error": "Product does not exist"}, status=404)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(
            user=request.user, completed=False)
        cartitem, created = CartItem.objects.get_or_create(
            cart=cart, product=product)

        cartitem.quantity += quantity
        cartitem.save()
        num_of_items = cart.cartitems.count()  # Get updated cart item count

        return JsonResponse({"num_of_items": num_of_items}, status=200)
    else:
        return JsonResponse({"error": "User not authenticated"}, status=401)


@transaction.atomic
def confirm_payment(request, pk):
    cart = Cart.objects.get(id=pk)
    cartitems = cart.cartitems.all()
    insufficient_stock_items = []

    for cartitem in cartitems:
        if cartitem.quantity > cartitem.product.quantity:
            insufficient_stock_items.append(cartitem.product.title)

    if insufficient_stock_items:
        messages.error(request, "Cannot proceed with payment. The following items exceed available stock: " + {
                       ', '.join(insufficient_stock_items)})
        return redirect("cart")

    if not cartitems:
        messages.error(
            request, "Cannot proceed with payment. No items in cart")
        return redirect("cart")

    # Mark the cart as completed
    cart.completed = True

    # Update product quantities
    for cartitem in cartitems:
        new_quantity = cartitem.product.quantity - cartitem.quantity
        cartitem.product.quantity = new_quantity
        cartitem.product.save()

    order = Orders(cart=cart)
    order.save()
    cart.save()

    messages.success(
        request, f"Payment made successfully. Cart reference number: {pk}")
    return redirect("home")


@require_http_methods(["DELETE"])
def delete_cart_item(request, pk):
    try:
        cart_item = CartItem.objects.get(id=pk)
        cart_item.delete()
        return JsonResponse({"success": True}, status=200)
    except CartItem.DoesNotExist:
        return JsonResponse({"error": "CartItem not found"}, status=404)

# Test function to check if the user is staff or admin


# Specify the required groups here
@group_required('sales', 'warehouse')
def product_portal(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'product_portal.html', context)


def forbidden(request):
    return render(request, '403.html', status=403)
