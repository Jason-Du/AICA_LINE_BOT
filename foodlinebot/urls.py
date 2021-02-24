from django.urls import path
from  foodlinebot import views

urlpatterns = [
    path('callback', views.callback)
]