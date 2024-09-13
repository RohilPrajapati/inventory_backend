from rest_framework import serializers
from datetime import datetime
from inventory.models import Stock, Transaction, TransactionItem, TransactionType
from django.db import transaction as db_transaction


class StockModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class TransactionTypeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionType
        fields = '__all__'

class TransactionItemModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionItem
        fields = '__all__'

class TransactionModelSerializer(serializers.ModelSerializer):
    transaction_item = TransactionItemModelSerializer()
    class Meta:
        model = Transaction
        fields = '__all__'

class CreateTransactionItem(serializers.Serializer):
    product = serializers.IntegerField()
    stock = serializers.IntegerField(required=False,allow_null=True)
    qty = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=12,decimal_places=2)

class CreateTransaction(serializers.Serializer):
    transaction_item = serializers.ListField(child=CreateTransactionItem(),allow_empty=False)
    transaction_type = serializers.IntegerField()
    supplier = serializers.IntegerField(required=False) #required for purchase only
    transaction_no = serializers.CharField() # purchase bill number if it exists
    notes = serializers.CharField()

    def handle_sales(self):
        last_trans_obj = Transaction.objects.filter(transaction_type = self.transaction_type).order_by('bill_no')
        order_no = int("%04d" % 1)
        current_year = datetime.today().year
        if last_trans_obj.transaction_date.year != current_year:
            order_no = 1
        else:
            order_no = last_trans_obj.order_no + 1

        bill_no = "SL/"+current_year+"/%05d"%order_no
        # TODO complete sales
        ...

    def handle_purchase(self,validated_data):
        with db_transaction.atomic():
            last_trans_objects = Transaction.objects.filter(transaction_type = validated_data['transaction_type']).order_by('bill_no')
            current_year = datetime.today().year
            print(current_year)
            if not last_trans_objects:
                order_no = 1
            if last_trans_objects.exists():
                last_trans_obj = last_trans_objects.first()
                if last_trans_obj.transaction_date.year != current_year:
                    order_no = 1
                elif last_trans_obj:
                    order_no = last_trans_obj.order_no + 1

            bill_no = f"PR/{current_year}/"+ "%05d" % order_no 
            transaction = Transaction.objects.create(
                    transaction_type_id = validated_data['transaction_type'],
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
                stock = Stock.objects.filter(product=item_data['product'], supplier=validated_data['supplier']).first()

                if stock:
                    # Update stock with the purchased quantity
                    stock.quantity_in_stock += item_data['qty']
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
            Stock.objects.bulk_update(stock_updates, ['quantity_in_stock', 'purchase_price'])

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
                total_amount += item_data['price']
            transaction.total_amount = total_amount
            transaction.save()
            # Bulk create transaction items
            TransactionItem.objects.bulk_create(transaction_items)
            

            return transaction

