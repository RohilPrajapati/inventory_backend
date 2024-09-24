from rest_framework import serializers
from django.utils import timezone
from inventory.models import Stock, Transaction, TransactionItem, TransactionType
from django.db import transaction as db_transaction
from django.shortcuts import get_object_or_404

class StockModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'
        depth = 1

class TransactionTypeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionType
        fields = '__all__'

class TransactionItemModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionItem
        fields = '__all__'
        depth = 1   

class TransactionModelSerializer(serializers.ModelSerializer):
    transaction_items = TransactionItemModelSerializer(many=True,read_only=True)
    class Meta:
        model = Transaction
        fields = '__all__'
        depth = 1

class CreateTransactionItem(serializers.Serializer):
    product = serializers.IntegerField()
    qty = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=12,decimal_places=2)

class CreateSalesTransactionItem(serializers.Serializer):
    product = serializers.IntegerField()
    stock = serializers.IntegerField(required=False,allow_null=True)
    qty = serializers.IntegerField()

class CreatePurchaseTransactionSerializer(serializers.Serializer):
    transaction_item = serializers.ListField(child=CreateTransactionItem(),allow_empty=False)
    supplier = serializers.IntegerField(required=False) #required for purchase only
    transaction_no = serializers.CharField() # purchase bill number if it exists
    notes = serializers.CharField()
    is_restock = serializers.BooleanField(default=False)

    def handle_purchase(self,validated_data):
        try:
            with db_transaction.atomic():
                last_trans_objects = Transaction.objects.filter(transaction_type = 1).order_by('order_no')
                current_year = timezone.now().year
                if not last_trans_objects:
                    order_no = 1
                if last_trans_objects.exists():
                    last_trans_obj = last_trans_objects.last()
                    order_no = last_trans_obj.order_no + 1
                    if last_trans_obj.transaction_date.year != current_year:
                        order_no = 1

                bill_no = f"PR/{current_year}/"+ "%05d" % order_no 
                transaction = Transaction.objects.create(
                        transaction_type_id = 1,
                        order_no = order_no,
                        transaction_no = validated_data['transaction_no'],
                        bill_no = bill_no,
                        notes = validated_data['notes']
                    )
                
                transaction_items = []
                stock_updates = []  
                new_stock = []
                
                # for items create bulk save()
                for item_data in validated_data['transaction_item']:
                    # Get or create stock for this product and supplier
                    stock = Stock.objects.filter(product=item_data['product'], supplier=validated_data['supplier']).last()

                    if stock and validated_data['is_restock']:
                        # Update stock with the purchased quantity
                        stock.quantity_in_stock += item_data['qty']
                        stock.updated_date = timezone.now()
                        stock_updates.append(stock)  # Add to update list
                    else:
                        # If no stock exists, create it
                        stock = Stock(
                            product_id=item_data['product'],
                            supplier_id=validated_data['supplier'],
                            quantity_in_stock=item_data['qty'],
                            purchase_price=item_data['price'],
                        )
                        new_stock.append(stock)  # Add to create list

                # if new stock in the purchase
                Stock.objects.bulk_create(new_stock)
                # Bulk create or update stock records
                Stock.objects.bulk_update(stock_updates, ['quantity_in_stock', 'purchase_price','updated_date'])

                total_amount = 0
                for item_data in validated_data['transaction_item']:
                    # Create a TransactionItem and append to the list
                    transaction_items.append(TransactionItem(
                        product_id=item_data['product'],
                        transaction=transaction,
                        stock=stock,
                        qty=item_data['qty'],
                        price=item_data['price']
                        
                    ))
                    amount = item_data['qty'] * item_data['price']
                    total_amount += amount
                # Bulk create transaction items
                TransactionItem.objects.bulk_create(transaction_items)

                transaction.total_amount = total_amount
                transaction.save()
                
                return transaction
        except Exception as e:
            raise Exception("Purchase Transaction Fail !")

class CreateSalesTransactionSerializer(serializers.Serializer):
    transaction_item = serializers.ListField(child=CreateSalesTransactionItem(),allow_empty=False)
    transaction_type = serializers.IntegerField()
    notes = serializers.CharField()

    def handle_sales(self,validated_data):
        try:
            with db_transaction.atomic():
                last_trans_objects = Transaction.objects.filter(transaction_type = validated_data['transaction_type']).order_by('order_no')
                current_year = timezone.now().year
                if not last_trans_objects:
                    order_no = 1
                if last_trans_objects.exists():
                    last_trans_obj = last_trans_objects.last()
                    order_no = last_trans_obj.order_no + 1
                    if last_trans_obj.transaction_date.year != current_year:
                        order_no = 1
                bill_no = f"SL/{current_year}/"+ "%05d" % order_no 

                transaction = Transaction.objects.create(
                        transaction_type_id = validated_data['transaction_type'],
                        order_no = order_no,
                        bill_no = bill_no,
                        notes = validated_data['notes']
                    )
                
                transaction_items = []
                stock_updates = []

                total_amount = 0
                for item_data in validated_data['transaction_item']:
                    # Create a TransactionItem and append to the list

                    stock = get_object_or_404(Stock,id=item_data['stock'])
                    # validate if the stock with order qty:
                    if stock.quantity_in_stock < item_data['qty']:
                        raise ValueError("Stock quantity is less then order quantity")

                    stock.quantity_in_stock -= item_data['qty']
                    stock.updated_date = timezone.now()
                    stock_updates.append(stock)

                    transaction_items.append(TransactionItem(
                        product_id=item_data['product'],
                        transaction=transaction,
                        stock=stock,
                        qty=item_data['qty'],
                        price=stock.sales_price
                    ))
                    total_amount += stock.sales_price
                # TODO updateing stock will update date for all the stock need to fix it
                Stock.objects.bulk_update(stock_updates, ['quantity_in_stock', 'purchase_price','updated_date'])
                # Bulk create transaction items
                TransactionItem.objects.bulk_create(transaction_items)

                transaction.total_amount = total_amount
                transaction.save()
                
                return transaction
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise Exception("Sales Transaction Fail !")