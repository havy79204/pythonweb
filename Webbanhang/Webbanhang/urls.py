"""Webbanhang URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
#load images 
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),  # Kết nối với URLs từ ứng dụng shop
]
if settings.DEBUG:  # Kiểm tra xem dự án có đang trong chế độ phát triển không
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




