from django.urls import path
from . import views

urlpatterns = [
    path('get_houses/', views.get_houses, name='get_houses'),
    path('create_house/', views.create_house, name='create_house'),
    path('my_houses/', views.my_houses, name='my_houses'),
    path('update_house/<int:house_id>/', views.update_house, name='update_house'),
    path('delete_house/<int:house_id>/', views.delete_house, name='delete_house'),
]