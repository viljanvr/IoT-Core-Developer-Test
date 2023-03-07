from django.urls import path
from . import views

urlpatterns = [
    path('', views.getAllBusses),
    path('<int:id>/', views.getBus)
]