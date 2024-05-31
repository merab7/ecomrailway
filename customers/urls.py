from django.contrib import admin
from django.urls import path
from .views import signup_view, profile, update_password, my_orders,  activate
from django.contrib.auth.models import User

urlpatterns = [
    path('signup/', signup_view, name="signup"),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('profile/', profile, name="profile"),
    path('update_password/', update_password, name="update_password"),
    path('my_orders/', my_orders, name="my_orders"),


]