# FILE: medisoft/urls.py
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentications Cluster Router Matrix
    path('', views.login_view, name='root'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Clinical Infrastructure Operational Nodes
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('appointments/', views.appointments_view, name='appointments'),
    path('book-slot/<int:slot_id>/', views.book_slot_view, name='book_slot'),
    path('beds/', views.beds_view, name='beds'),
    path('pharmacy/', views.pharmacy_view, name='pharmacy'),
    path('blood/', views.blood_view, name='blood'),
    path('symptom-checker/', views.symptom_checker_view, name='symptom_checker'),
    path('profile/', views.profile_view, name='profile'),
]