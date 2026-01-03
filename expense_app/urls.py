from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('home/', views.home, name='home'),
    path('register_page/', views.register_page, name='register_page'),
    path('edit_expense/<int:pk>/', views.edit_expense, name='edit_expense'),
    path('delete_expense/<int:pk>/', views.delete_expense, name='delete_expense'),
]

