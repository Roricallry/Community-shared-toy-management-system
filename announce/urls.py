from django.urls import path
# from .views import announcement_list, announcement_create, announcement_update, announcement_delete,announcement_detail,announcement_user
from .views import *
urlpatterns = [
    path('announcement_list/', announcement_list, name='announcement'),
    path('create_announce/', announcement_create, name='announcement_create'),
    path('update_announce/<int:pk>/', announcement_update, name='announcement_update'),
    path('delete_announce/<int:pk>/', announcement_delete, name='announcement_delete'),
    path('detail_announce/<int:pk>/', announcement_detail, name='announcement_detail'),
    # path('user_annonounce/<int:pk>', announcement_user, name='user_announcement'),
    path('announcement_user/', announcement_user, name='announcement_user'),
]