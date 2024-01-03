from django.urls import path

from sales_chain.apps import SalesChainConfig

from sales_chain.views import SupplierView, ProductView, SupplierEditView, ProductEditView

app_name = SalesChainConfig.name

urlpatterns = [
    path('suppliers/', SupplierView.as_view(), name='suppliers'),
    path('suppliers/<int:supplier_id>/', SupplierEditView.as_view(), name='one_supplier'),
    path('products/', ProductView.as_view(), name='products'),
    path('products/<int:product_id>/', ProductEditView.as_view(), name='one_product'),

]