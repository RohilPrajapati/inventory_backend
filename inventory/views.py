from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Stock, Transaction, TransactionItem,TransactionType
from .serializers import *


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

class InventoryListView(APIView):
    def get(self, request):
        search = request.GET.get('search',None)
        stock = Stock.objects.all()
        if search is not None:
            stock = stock.filter(product__name__icontains=search) | \
                stock.filter(supplier__name__icontains=search)
        serializer = StockModelSerializer(stock, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TransactionListView(APIView):
    def get(self, request):
        search = request.GET.get('search',None)
        transaction_type = request.GET.get('transaction_type',None)
        transaction = Transaction.objects.select_related('transaction_items')
        if search is not None:
            transaction = transaction.filter(product__name__icontains=search) | \
                    transaction.filter(supplier__name__icontains=search) | \
                transaction.filter(transaction_type__name__icontains=search)
        serializer = TransactionTypeModelSerializer(transaction_type, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request):
        serializer = CreateTransaction(data=request.data)
        print(request.data)
        if serializer.is_valid(raise_exception=True):
            if serializer.validated_data['transaction_type'] == 1:
                # purchase -> stock update
                serializer.handle_purchase(serializer.validated_data)
            elif serializer.validated_data['transaction_type'] == 2:
                # sales -> stock update
                ...
            # TODO 
            # purchase return -> stock update
            # sales return -> stock update
            # serializer.save()
            return Response({"message":"Testing"},status=status.HTTP_201_CREATED)





