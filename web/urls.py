from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .views import logout_view


urlpatterns = [
    path('', views.home_view, name='home'),
    path('hakkimizda/', views.about_view, name='about'),
    path('iletisim/', views.contact_view, name='contact'),
    path('randevu/', views.appointment_create, name='appointment'),
    path('yorumlar/', views.comments_view, name='comments'),
    path('randevu-basari/<str:order_number>/', views.appointment_success, name='appointment_success'),
    path('siparis-takip/', views.track_order_view, name='track_order'),
    path('siparis-sonuc/<str:tracking_code>/', views.track_order_result_view, name='track_order_result'),

    # Admin paneli ana sayfa ve alt sayfalar
    path('admin-panel/', views.admin_home, name='admin_home'),  # admin anasayfa
    path('admin-panel/appointments/', views.admin_appointments, name='admin_appointments'),
    path('admin-panel/carpets/', views.admin_carpets, name='admin_carpets'),
    path('admin-panel/comments/', views.admin_comments, name='admin_comments'),

    # AJAX işlemleri için
    path('admin-panel/comment/<int:comment_id>/approve/', views.approve_comment, name='approve_comment'),
    path('admin-panel/carpet/<int:carpet_id>/update/', views.update_carpet_status, name='update_carpet_status'),
    path('admin-panel/carpet/<int:carpet_id>/delete/', views.delete_carpet, name='delete_carpet'),

    # Giriş
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]
