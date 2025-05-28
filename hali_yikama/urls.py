from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),          # Admin paneli
    path('', include('web.urls')),            # Anasayfa ve diğer sayfalar (web app)
    path('takip/', include('core.urls')),     # Halı takip işlemleri (core app)
]
