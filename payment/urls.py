from django.urls import path
from .views import initiate_payment, callback, verify_coupon, payment

urlpatterns = [
    path('pay/', initiate_payment, name='pay'),
    path('payment/', payment, name='payment'),
    path('callback/', callback, name='callback'),
    path('verify_coupon', verify_coupon, name = 'verify_coupon'),
]