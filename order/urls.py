from django.urls import path

from .views import execute, orderStock,market
from django.urls import path

urlpatterns = [
    path('order',orderStock.as_view()),
    path('market',market.as_view()),
    path('execute',execute.as_view()),
]
