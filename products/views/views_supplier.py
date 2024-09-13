from rest_framework.views import APIView
from rest_framework  import status
from products.models import Supplier
from products.serializers import SupplierModelSerializer
from backend.paginations import PagePaginationCustom
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import IntegrityError

class SupplierListView(APIView, PagePaginationCustom):
    def get(self, request):
        supplier = Supplier.objects.all()
        search = request.GET.get('search')
        if search is not None:
            supplier = supplier.filter(name__icontains=search) | \
                       supplier.filter(phone_number__icontains=search) | \
                       supplier.filter(email__icontains=search) | \
                       supplier.filter(address__icontains=search)

        result = self.paginate_queryset(supplier, request)
        serializer = SupplierModelSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = SupplierModelSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = {
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)


class SupplierDetailView(APIView):
    def get(self, request, pk):
        supplier = get_object_or_404(Supplier,id =pk)
        serializer = SupplierModelSerializer(supplier)
        response = {
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    def put(self, request, pk):
        supplier = get_object_or_404(Supplier,id =pk)
        serializer = SupplierModelSerializer(supplier,data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = {
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            supplier = get_object_or_404(Supplier,id =pk)
            supplier.delete()
            response = {
                "message": "Supplier has been deleted."
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)
        except IntegrityError:
            response = {
                'message': 'Please Contact Administration'
            }
            return Response(response, status=status.HTTP_200_OK)
