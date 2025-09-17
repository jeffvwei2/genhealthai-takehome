from django.urls import path, include

urlpatterns = [
    path('upload/', include('api.uploads.urls')),
    path('orders/', include('api.orders.urls')),
]
