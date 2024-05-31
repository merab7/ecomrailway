from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:pk>', views.details, name='details'),
    path('product/<cat_name>', views.category, name='category'),
    path('quantity', views.quantity, name='quantity'),
    path('max_quantity', views.max_quantity, name='max_quantity'),
    path('set_language/<str:lang_code>/', views.set_language, name='set_language'),
]