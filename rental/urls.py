from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomLoginView
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('', views.home, name='home'),
    path('cars/', views.car_list, name='car_list'),
    path('cars/<int:car_id>/book/', views.book_car, name='book_car'),
    path('booking/confirmation/<int:booking_id>', views.booking_confirmation, name='booking_confirmation'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('profile/', views.user_profile, name='user_profile'),   
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),  # make sure you already have this    
]
