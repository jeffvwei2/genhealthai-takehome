from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['patient_first_name', 'patient_last_name', 'dob', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['patient_first_name', 'patient_last_name']
    ordering = ['-created_at']
