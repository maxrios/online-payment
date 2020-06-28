from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('addcard/', views.add_card, name='addcard')
]
