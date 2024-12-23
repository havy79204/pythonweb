# Generated by Django 4.1.13 on 2024-12-06 14:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DatHang',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ngay_dat_hang', models.DateTimeField(auto_now_add=True)),
                ('hoan_thanh', models.BooleanField(default=False, null=True)),
                ('luu_thong_tin_dat_hang_id', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SanPham',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ten', models.CharField(max_length=200, null=True)),
                ('gia', models.FloatField()),
                ('ky_thuat_so', models.BooleanField(default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='KhachHang',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ten', models.CharField(max_length=200, null=True)),
                ('email', models.CharField(max_length=200, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DiaChiGiaoHang',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia_chi', models.CharField(max_length=200, null=True)),
                ('thanh_pho', models.CharField(max_length=200, null=True)),
                ('tinh_thanh', models.CharField(max_length=200, null=True)),
                ('so_dien_thoai', models.CharField(max_length=10, null=True)),
                ('ngay_dat_hang', models.DateTimeField(auto_now_add=True)),
                ('dat_hang', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.dathang')),
                ('khach_hang', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.khachhang')),
            ],
        ),
        migrations.CreateModel(
            name='DatNhieuHang',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('so_luong_mua', models.IntegerField(blank=True, default=0, null=True)),
                ('ngay_dat_hang', models.DateTimeField(auto_now_add=True)),
                ('dat_hang', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.dathang')),
                ('san_pham', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.sanpham')),
            ],
        ),
        migrations.AddField(
            model_name='dathang',
            name='khach_hang',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.khachhang'),
        ),
    ]
