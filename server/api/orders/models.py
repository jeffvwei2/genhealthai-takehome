from django.db import models

class Order(models.Model):
    patient_first_name = models.CharField(max_length=100)
    patient_last_name = models.CharField(max_length=100)
    dob = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('new', 'New'),
        ('processing', 'Processing'),
        ('complete', 'Complete'),
    ], default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient_first_name} {self.patient_last_name}"
