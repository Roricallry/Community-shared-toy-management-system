from . import views
from toy import views as toy_views
from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('login/admin/', views.default_announce, name='login_admin'),
    path('register/', views.user_register, name='register'),
    path('personal_homepage/', views.personal_homepage, name='personal_homepage'),
    path('admin_info/', views.admin_info, name='admin_info'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('change_password/', auth_views.PasswordChangeView.as_view(template_name='registration/change_password.html'),
         name='change_password'),
    path('change_password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration'
                                                                                          '/change_password_done.html'),
         name='password_change_done'),
    path('change_contact_information/', views.change_contact_information, name='change_contact_information'),
    path('about_us/', views.about_us, name='about_us'),

    path('manage_owners/', views.manage_owners, name='manage_owners'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('reset_password/<int:user_id>/', views.reset_password, name='reset_password'),
    path('confirm_reset_password/<int:user_id>/', views.confirm_reset_password, name='confirm_reset_password'),
    path('export_users_to_excel', views.export_users_to_excel, name='export_users_to_excel'),
    path('view_donations/', views.view_donations, name='view_donations'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
]
