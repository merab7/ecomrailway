from django.contrib import admin
from django.urls import path
from .views import cart_sum, cart_add, cart_del, edit, update
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User

urlpatterns = [
    path('sum/', cart_sum, name='cart_sum' ),
    path('add/',cart_add, name='cart_add'),
    path('edit/<int:id>/<size>/',edit, name='edit'),
    path('delete/<int:id>/<size>/', cart_del, name='cart_del'),
    path('update/', update, name='update'),
]