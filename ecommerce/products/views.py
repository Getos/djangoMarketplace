from rest_framework import authentication, generics, permissions
from .models import Product
from .seralizers import ProductSerializer
from .models import Product
from .permissions import isStaffEditorPermisson
from django.contrib.auth.models import User


class ProductListCreateAPIView(
        generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [isStaffEditorPermisson,]

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title
        serializer.save()


product_list_create_view = ProductListCreateAPIView.as_view()


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = 'pk'
    authentication_classes = [authentication.TokenAuthentication]


product_detail_view = ProductDetailAPIView.as_view()


class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [isStaffEditorPermisson]

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title
  # Debug output
        user = self.request.user
        print(f'Update User: {user.username}')
        print(f'Is Staff: {user.is_staff}')
        print(f'Is Admin: {user.is_superuser}')
        permissions = user.user_permissions.all()
        print('User Permissions:')
        for perm in permissions:
            print(perm.name)


product_update_view = ProductUpdateAPIView.as_view()


class ProductDestroyAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [isStaffEditorPermisson]

    def perform_destroy(self, instance):
        # You can access the user and print permissions here
        user = self.request.user
        permissions = user.user_permissions.all()
        print(f'User: {user.username}')
        print(f'Is Admin: {user.is_superuser}')
        print(f'Is Staff: {user.is_staff}')
        print('User Permissions:')
        for perm in permissions:
            print(perm.name)
        # # Check if user has admin permissions here
        # if not user.is_superuser:
        #     raise PermissionDenied(
        #         "You do not have permission to perform this action.")

        return super().perform_destroy(instance)


product_delete_view = ProductDestroyAPIView.as_view()
