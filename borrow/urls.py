from django.urls import path
from . import views


urlpatterns = [
    path('borrow_query/', views.borrow_query, name='borrow_query'),
    path('borrow_create/', views.borrow_create, name='borrow_create'),
    path('borrow_cancel/', views.borrow_cancel, name='borrow_cancel'),
    path('borrow_update/', views.borrow_update, name='borrow_update'),
    path('export_borrow_to_excel/', views.export_borrow_to_excel, name="export_borrow_to_excel"),
    path('count/', views.most_borrowed_toys, name='most_borrowed_toys'),
    path('test/', views.test, name='test'),
]