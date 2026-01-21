from django.urls import path
from . import views

urlpatterns = [
    path('create_order/', views.create_order, name='create_order'),
    path('get_sales_records/', views.get_sales_records, name='get_sales_records'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('my_sales/', views.my_sales, name='my_sales'),
    path('sales_stats/', views.sales_stats, name='sales_stats'),
    path('create_payment/', views.create_payment, name='create_payment'),
    path('payment_callback/', views.payment_callback, name='payment_callback'),
]
