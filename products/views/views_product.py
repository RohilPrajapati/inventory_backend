from rest_framework.views import APIView
from rest_framework  import status
from products.models import Product
from products.serializers import ProductModelSerializer
from backend.paginations import PagePaginationCustom
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from rest_framework.parsers import MultiPartParser,JSONParser

class ProductListView(APIView, PagePaginationCustom):
    parser_classes = [MultiPartParser,JSONParser]
    def get(self, request):
        product = Product.objects.all()
        search = request.GET.get('search')
        if search is not None:
            product = product.filter(name__icontains=search) | \
                       product.filter(description__icontains=search) | \
                       product.filter(brand__name__icontains=search) | \
                       product.filter(category__name__icontains=search) | \
                       product.filter(color__icontains=search) | \
                       product.filter(weight__icontains=search) | \
                       product.filter(size__icontains=search) | \
                       product.filter(dimensions__icontains=search) | \
                       product.filter(sku__icontains=search) | \
                       product.filter(upc__icontains=search) | \
                       product.filter(address__icontains=search)

        result = self.paginate_queryset(product, request)
        serializer = ProductModelSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = ProductModelSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.validated_data['created_by'] = serializer.validated_data['category']
            serializer.validated_data['created_by'] = request.user
            serializer.save()
            response = {
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)


class ProductDetailView(APIView):
    parser_classes = [MultiPartParser,JSONParser]
    def get(self, request, pk):
        product = get_object_or_404(Product,id =pk)
        serializer = ProductModelSerializer(product)
        response = {
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    def put(self, request, pk):
        product = get_object_or_404(Product,id =pk)
        serializer = ProductModelSerializer(product,data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = {
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            product = get_object_or_404(Product,id =pk)
            product.delete()
            response = {
                "message": "Product has been deleted."
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)
        except IntegrityError:
            response = {
                'message': 'Please Contact Administration'
            }
            return Response(response, status=status.HTTP_200_OK)
