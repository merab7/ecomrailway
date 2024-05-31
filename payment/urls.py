from django.urls import path
from . import views


urlpatterns = [
    path('payment_success', views.payment_success, name='payment_success'),
    path('ch_out', views.checkout, name='ch_out'),
    path('billing', views.billing, name='billing'),
    path('proc_order', views.proc_order, name='proc_order'),

]