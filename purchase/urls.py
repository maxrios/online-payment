from django.urls import path
from . import views


urlpatterns = [
    path('create/', views.create_purchase, name='create-purchase'),
    path('admin-all/', views.view_all_purchases, name='all-purchases')
]