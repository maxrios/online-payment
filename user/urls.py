from django.urls import path
from card.views import add_card, remove_card
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('addcard/', add_card, name='addcard'),
    path('removecard/', remove_card, name='removecard')
]
