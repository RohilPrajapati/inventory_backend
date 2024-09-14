from django.urls import path
from .views import TransactionListView,CreatePurchaseView
urlpatterns = [
    path('', TransactionListView.as_view(),name='transaction_list'),
    path('purchase/', CreatePurchaseView.as_view(),name='transaction_list'),
]