from django.db import models
from django.contrib.auth.models import User

class KhachHang(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=False)
    ten = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.ten if self.ten else "Khách hàng không tên"
class SanPham(models.Model):
    ten = models.CharField(max_length=200, null=True)
    gia = models.FloatField()
    ky_thuat_so = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(upload_to='sanpham_images/', blank=True, null=True)
    def __str__(self):
        return self.ten
    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return ''
class DatHang(models.Model):
    khach_hang = models.ForeignKey(KhachHang, on_delete=models.SET_NULL, blank=True, null=True)
    ngay_dat_hang = models.DateTimeField(auto_now_add=True)
    hoan_thanh = models.BooleanField(default=False, null=True, blank=False)
    ma_dat_hang = models.CharField(max_length=200, null=True)  # Đảm bảo rằng cột này đã tồn tại trong cơ sở dữ liệu

    def __str__(self):
        return str(self.id)

    def total_price(self):
        return sum(item.san_pham.gia * item.so_luong_mua for item in self.datnhieuhang_set.all())

class DatNhieuHang(models.Model):
    san_pham = models.ForeignKey(SanPham, on_delete=models.CASCADE, null=True, blank=True)
    dat_hang = models.ForeignKey(DatHang, on_delete=models.CASCADE, null=True, blank=True)
    so_luong_mua = models.IntegerField(default=0, null=True, blank=True)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.san_pham.ten} - Số lượng: {self.so_luong_mua}"
    @property
    def get_total_price(self):
        """Tính tổng giá của sản phẩm trong giỏ."""
        return self.san_pham.gia * self.so_luong_mua
class DiaChiGiaoHang(models.Model):
    khach_hang = models.ForeignKey(KhachHang, on_delete=models.CASCADE, blank=True, null=True)
    dat_hang = models.ForeignKey(DatHang, on_delete=models.CASCADE, blank=True, null=True)
    dia_chi = models.CharField(max_length=200, null=True)
    thanh_pho = models.CharField(max_length=200, null=True)
    tinh_thanh = models.CharField(max_length=200, null=True)
    so_dien_thoai = models.CharField(max_length=10, null=True)
    ngay_tao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.dia_chi} - {self.khach_hang.ten if self.khach_hang else 'Khách vãng lai'}"
