# from products.models import Product
# from products.seralizers import ProductSerializer

# from rest_framework.decorators import api_view
# from rest_framework.response import Response


# @api_view(["POST"])
# def api_home(request, *args, **kwargs):
#     seralizer = ProductSerializer(data=request.data)
#     if seralizer.is_valid(raise_exception=True):
#         print(seralizer.data)
#         return Response(seralizer.data)
#     return Response({"invalid": "not good data"}, status=400)
