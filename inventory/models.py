import uuid

from django.db import models

from products.models import Product, Supplier


# Create your models here.

class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='stocks_product')
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='stocks_supplier',null=True)
    quantity_in_stock = models.IntegerField(default=0)
    minimum_stock_level = models.IntegerField(default=10)
    maximum_stock_level = models.IntegerField(default=50)
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sales_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_restock = models.BooleanField(default=False)
    warehouse_location = models.CharField(max_length=100, default='')
    aisle = models.CharField(max_length=100, default='')
    shelf = models.CharField(max_length=100, default='')
    bin = models.BooleanField(default=False)
    updated_date = models.DateTimeField(null=True)

class TransactionType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=True)


class Transaction(models.Model):
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.PROTECT, related_name="transaction")
    supplier = models.ForeignKey(Supplier,on_delete = models.PROTECT)
    transaction_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    transaction_no = models.CharField(max_length=100,null=True)
    order_no = models.IntegerField(default=0)
    bill_no = models.CharField(unique=True,max_length=100)
    transaction_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(default='')
    total_amount = models.DecimalField(max_digits=12,decimal_places=2,default=0)

class TransactionItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='transaction_product')
    transaction = models.ForeignKey(Transaction, on_delete=models.PROTECT, related_name='transaction_items')
    stock = models.ForeignKey(Stock, on_delete=models.SET_NULL, null=True, related_name='transaction_stock')
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
