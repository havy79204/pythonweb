from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *

# Trang chủ - hiển thị danh sách sản phẩm
def home(request):
    san_pham_list = SanPham.objects.all()  # Lấy toàn bộ danh sách sản phẩm
    context = {'san_pham_list': san_pham_list}
    return render(request, 'shop/home.html', context)

# Trang giỏ hàng
def cart(request):
    if request.user.is_authenticated:  # Kiểm tra nếu người dùng đã đăng nhập
        khach_hang, created = KhachHang.objects.get_or_create(user=request.user)  # Lấy hoặc tạo khách hàng
        don_hang, created = DatHang.objects.get_or_create(khach_hang=khach_hang, hoan_thanh=False)  # Đơn hàng chưa hoàn thành
        items = don_hang.datnhieuhang_set.all()  # Lấy các mục sản phẩm trong giỏ hàng
        context = {'items': items, 'donhang': don_hang}
        return render(request, 'shop/cart.html', context)
    else:
        # Xử lý giỏ hàng cho khách vãng lai (không đăng nhập)
        items = []
        don_hang = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {'items': items, 'don_hang': don_hang}
    return render(request, 'shop/cart.html', context)

# Trang thanh toán
def checkout(request):
    if request.user.is_authenticated:  # Kiểm tra nếu người dùng đã đăng nhập
        khach_hang, created = KhachHang.objects.get_or_create(user=request.user)
        don_hang, created = DatHang.objects.get_or_create(khach_hang=khach_hang, hoan_thanh=False)
        items = don_hang.datnhieuhang_set.all()
    else:
        items = []
        don_hang = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {'items': items, 'don_hang': don_hang}
    return render(request, 'shop/checkout.html', context)

# Trang hồ sơ cá nhân
def profile(request):
    if request.user.is_authenticated:
        khach_hang = KhachHang.objects.filter(user=request.user).first()
        context = {
            "user": request.user.username,
            "email": request.user.email,
            "ten": khach_hang.ten if khach_hang else "",
        }
    else:
        context = {"user": "vy792004", "email": "Chưa đăng nhập"}

    return render(request, 'shop/profile.html', context)
