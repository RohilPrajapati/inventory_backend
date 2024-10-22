from django.urls import path
from .views import *

urlpatterns = [
    path('', TransactionListView.as_view(),name='transaction_list'),
    path('stock/', InventoryListView.as_view(),name='transaction_list'),
    path('stock/product/<int:product_id>/', ProductWiseInventoryView.as_view(),name='transaction_list'),
    path('purchase/', CreatePurchaseView.as_view(),name='create_purchase'),
    path('sales/', CreateSalesView.as_view(),name='create_sales'),
]