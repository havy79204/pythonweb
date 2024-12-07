from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Trang chủ
    path('cart/', views.cart, name='cart'),  # Giỏ hàng
    path('checkout/', views.checkout, name='checkout'),  # Thanh toán
    path('profile/', views.profile, name='profile'),  # Trang profile
]
