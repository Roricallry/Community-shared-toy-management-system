from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='user_home'),
    path('toy_list/', views.toy_list, name='toy_list'),
    path('toys/edit/<int:toy_id>/', views.toy_edit, name='toy_edit'),
    path('toy_delete/', views.toy_delete, name='toy_delete'),
    path('toy_add/', views.toy_add, name='toy_add'),
    path('export_toys_to_excel', views.export_toys_to_excel, name='export_toys_to_excel'),
]