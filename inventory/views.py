from django.shortcuts import get_object_or_404,get_list_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Stock, Transaction, TransactionItem,TransactionType
from .serializers import *
from backend.paginations import PagePaginationCustom
from django.utils import timezone
from datetime import datetime

class TransactionTypeListView(APIView):
    def get(self, request):
        transaction_types = TransactionType.objects.all()
        return Response(TransactionTypeModelSerializer(transaction_types, many=True).data,status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TransactionTypeModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

class TransactionTypeDetailView(APIView):
    def get(self,request,pk):
        transaction_type = get_object_or_404(TransactionType,pk=pk)
        return Response(TransactionTypeModelSerializer(transaction_type).data,status=status.HTTP_200_OK)

    def put(self,request,pk):
        transaction_type = get_object_or_404(TransactionType,pk=pk)
        serializer = TransactionTypeModelSerializer(transaction_type,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)

    def delete(self,request,pk):
        transaction_type = get_object_or_404(TransactionType,pk=pk)
        transaction_type.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class InventoryListView(APIView,PagePaginationCustom):
    def get(self, request):
        search = request.GET.get('search',None)
        stock = Stock.objects.all()
        if search is not None:
            stock = stock.filter(product__name__icontains=search) | \
                stock.filter(supplier__name__icontains=search)
        result = self.paginate_queryset(stock, request)
        serializer = StockModelSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)

class ProductWiseInventoryView(APIView):
    def get(self,request,product_id):
        stock = get_list_or_404(Stock,product_id=product_id)
        serializer = StockModelSerializer(stock,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class TransactionListView(APIView,PagePaginationCustom):
    def get(self, request):
        try:
            current_date = timezone.now().date().strftime('%Y-%m-%d')
            search = request.GET.get('search',None)
            transaction_type = request.GET.get('transaction_type',None)
            from_date_str = request.GET.get('from_date',current_date)
            to_date_str = request.GET.get('to_date',current_date)
            from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
            to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()
            print(from_date)
            print(to_date)
            transaction = Transaction.objects.prefetch_related('transaction_items')
            if transaction_type:
                transaction = transaction.filter(transaction_type=transaction_type)
            
            transaction = transaction.filter(transaction_date__date__gte = from_date, transaction_date__date__lte = to_date)
                
            if search is not None:
                transaction = transaction.filter(product__name__icontains=search) | \
                        transaction.filter(supplier__name__icontains=search) | \
                    transaction.filter(transaction_type__name__icontains=search)
            transaction = transaction.order_by('-transaction_date')
            result = self.paginate_queryset(transaction, request)
            serializer = TransactionModelSerializer(result, many=True)
            return self.get_paginated_response(serializer.data)
        except (ValueError, TypeError) as e:
            return Response({'error': 'Invalid date format. Please provide valid dates.'}, status=400)

    

class CreatePurchaseView(APIView):
    def post(self,request):
        serializer = CreatePurchaseTransactionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.handle_purchase(serializer.validated_data)
            response = {
                "message":"Create purchase successfully !"
            }
            return Response(response,status=status.HTTP_201_CREATED)
        
class CreateSalesView(APIView):
    def post(self,request):
        serializer = CreateSalesTransactionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                serializer.handle_sales(serializer.validated_data)
                response = {
                    "message":"Create Sales successfully !"
                }
                return Response(response,status=status.HTTP_201_CREATED)
            except ValueError as ve:
                response = {
                    "message":f"{ve}"
                }
                return Response(response,status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(e)
                response = {
                    "message":"Something went wrong. Working on it !"
                }
                return Response(response,status=status.HTTP_400_BAD_REQUEST)
