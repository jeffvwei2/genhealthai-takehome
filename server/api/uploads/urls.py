from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health_check'),
    path('', views.upload_pdf, name='upload_pdf'),
]
