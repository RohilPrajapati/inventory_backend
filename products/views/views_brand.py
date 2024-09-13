from rest_framework.views import APIView
from rest_framework  import status
from products.models import Brand
from products.serializers import BrandModelSerializer
from backend.paginations import PagePaginationCustom
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import IntegrityError

class BrandListView(APIView, PagePaginationCustom):
    def get(self, request):
        brand = Brand.objects.all()
        search = request.GET.get('search')
        if search is not None:
            brand = brand.filter(name__icontains=search) | \
                       brand.filter(description__icontains=search) | \
                       brand.filter(address__icontains=search)

        result = self.paginate_queryset(brand, request)
        serializer = BrandModelSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = BrandModelSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = {
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)


class BrandDetailView(APIView):
    def get(self, request, pk):
        brand = get_object_or_404(Brand,id =pk)
        serializer = BrandModelSerializer(brand)
        response = {
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    def put(self, request, pk):
        brand = get_object_or_404(Brand,id =pk)
        serializer = BrandModelSerializer(brand,data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = {
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            brand = get_object_or_404(Brand,id =pk)
            brand.delete()
            response = {
                "message": "Brand has been deleted."
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)
        except IntegrityError:
            response = {
                'message': 'Please Contact Administration'
            }
            return Response(response, status=status.HTTP_200_OK)
