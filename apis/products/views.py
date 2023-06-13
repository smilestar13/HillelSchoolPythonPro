from rest_framework import generics
from rest_framework.permissions import AllowAny

from apis.products.serializers import ProductListSerializer, ProductDetailSerializer
from products.models import Product


class ProductList(generics.ListAPIView):
    queryset = Product.objects.prefetch_related('categories').all()
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]


class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.prefetch_related('categories').all()
    serializer_class = ProductDetailSerializer
    permission_classes = [AllowAny]