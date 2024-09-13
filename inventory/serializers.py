from rest_framework import serializers

from inventory.models import Stock, Transaction, TransactionItem, TransactionType


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

class CreateTransaction(serializers.Serializer):
    transaction_item = serializers.ListField(child=TransactionItemModelSerializer(many=True),allow_empty=False)
    transaction_type = serializers.IntegerField()
    notes = serializers.CharField()


