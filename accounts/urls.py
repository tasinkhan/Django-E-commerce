from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset_password_validation/<uidb64>/<token>/', views.reset_password_validation, name='reset_password_validation'),
    path('reset-password/', views.reset_password, name='reset_password'),
    
]