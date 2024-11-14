from django.urls import path
from . import views

urlpatterns = [
    path('inquire/', views.Toy_Inquire, name='Toy_Inquire'),
    path('create/', views.Toy_Create, name='Toy_Create'),
    path('update/<int:id>/', views.Toy_Update, name='Toy_Update'),
    path('delete/<int:id>/', views.Toy_Delete, name='Toy_Delete'),
    path('search/', views.Toy_Search, name='Toy_Search'),
]