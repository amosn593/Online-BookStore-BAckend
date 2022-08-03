from django.db.models import Q
from django.http import Http404

from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.decorators import api_view,  permission_classes
from rest_framework.response import Response

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class LatestProductsList(APIView):

    def get(self, request, format=None):
        products = Product.objects.all()[0:4]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetail(APIView):
    permission_classes = (permissions.AllowAny,)

    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class CategoryDetail(APIView):
    permission_classes = (permissions.AllowAny,)

    def get_object(self, category_slug):
        try:
            return Category.objects.filter(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def search(request, search):

    try:
        products = Product.objects.filter(
            Q(name__icontains=search) | Q(description__icontains=search))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    except:
        return Response({"products": []})
