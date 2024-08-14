
from django.http import JsonResponse
from django.shortcuts import redirect, render
from products.models import Product
import json
from users.models import Cart, CartItem
from django.contrib import messages


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

# def cart(request):
#     cart = None
#     cartitems = []
#     # Use cartcount to get the number of items
#     num_of_items = cartcount(request)

#     if request.user.is_authenticated:
#         cart, created = Cart.objects.get_or_create(
#             user=request.user, completed=False)
#         cartitems = cart.cartitems.all()

#     context = {
#         "cart": cart,
#         "items": cartitems,
#         "num_of_items": num_of_items
#     }
#     return render(request, "cart.html", context)


def add_to_cart(request):
    data = json.loads(request.body)
    product_id = data["id"]
# Default to 1 if quantity is not provided
    quantity = data.get("quantity", 1)

# Retrieve the product using the product_id
    try:
        product = Product.objects.get(id=product_id)
        print(f"product queryset {product}")
        available_quantity = product.quantity
        print(f"Cart Quantity: {quantity}, Available Quantity: {
              available_quantity}")

        # Compare the cart quantity with the available quantity
        if quantity > available_quantity:
            messages.success(request, f"quantity value {
                             quantity} is higher than avilable")
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


# def confirm_payment(request, pk):
#     cart = Cart.objects.get(id=pk)
#     cart.completed = True
#     cart.save()
#     messages.success(
#         request, f"payment made successfully reference number : {pk}")
#     return redirect("home")
def confirm_payment(request, pk):
    cart = Cart.objects.get(id=pk)
    cartitems = cart.cartitems.all()
    insufficient_stock_items = []

    # Check each cart item's quantity against the available product stock
    for cartitem in cartitems:
        if cartitem.quantity > cartitem.product.quantity:
            insufficient_stock_items.append(cartitem.product.title)

    if insufficient_stock_items:
        # If there are items with insufficient stock, show an error
        messages.error(request, f"Cannot proceed with payment. The following items exceed available stock: {
                       ', '.join(insufficient_stock_items)}")
        return redirect("cart")

    # If all items are within stock, proceed with payment
    cart.completed = True
    cart.save()
    messages.success(
        request, f"Payment made successfully. Reference number: {pk}")
    return redirect("home")
