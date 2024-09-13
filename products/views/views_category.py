from rest_framework.views import APIView
from rest_framework  import status
from products.models import Category
from products.serializers import CategoryModelSerializer
from backend.paginations import PagePaginationCustom
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import IntegrityError

class CategoryListView(APIView, PagePaginationCustom):
    def get(self, request):
        category = Category.objects.all()
        search = request.GET.get('search')
        if search is not None:
            category = category.filter(name__icontains=search) | \
                       category.filter(description__icontains=search) | \
                       category.filter(address__icontains=search)

        result = self.paginate_queryset(category, request)
        serializer = CategoryModelSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = CategoryModelSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = {
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)


class CategoryDetailView(APIView):
    def get(self, request, pk):
        category = get_object_or_404(Category,id =pk)
        serializer = CategoryModelSerializer(category)
        response = {
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    def put(self, request, pk):
        category = get_object_or_404(Category,id =pk)
        serializer = CategoryModelSerializer(category,data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = {
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            category = get_object_or_404(Category,id =pk)
            category.delete()
            response = {
                "message": "Category has been deleted."
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)
        except IntegrityError:
            response = {
                'message': 'Please Contact Administration'
            }
            return Response(response, status=status.HTTP_200_OK)
