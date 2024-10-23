from django.urls import path
from .views import views_supplier,views_brand,views_category,views_product 


urlpatterns = [
    path('', views_product.ProductListView.as_view(),name='product_list'),
    path('stock/', views_product.FetchProductWithStock.as_view(),name='product_list_with_stock'),
    path('<int:pk>/', views_product.ProductDetailView.as_view(), name='product_detail'),
    path('brand/', views_brand.BrandListView.as_view(),name='brand_list'),
    path('brand/<int:pk>/', views_brand.BrandDetailView.as_view(), name='brand_detail'),
    path('category/', views_category.CategoryListView.as_view(),name='category_list'),
    path('category/<int:pk>/', views_category.CategoryDetailView.as_view(), name='category_detail'),
    path('supplier/', views_supplier.SupplierListView.as_view(),name='supplier_list'),
    path('supplier/<int:pk>/', views_supplier.SupplierDetailView.as_view(), name='supplier_detail'),
]