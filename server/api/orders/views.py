from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Order
from datetime import datetime

@api_view(['GET', 'POST'])
def orders_list(request):
    """Handle orders - GET all orders, POST create new order"""
    if request.method == 'GET':
        orders = Order.objects.all().order_by('-created_at')
        data = []
        for order in orders:
            data.append({
                'id': order.id,
                'patient_first_name': order.patient_first_name,
                'patient_last_name': order.patient_last_name,
                'dob': order.dob.isoformat() if order.dob else None,
                'status': order.status,
                'created_at': order.created_at.isoformat(),
                'updated_at': order.updated_at.isoformat()
            })
        return Response(data)
    
    elif request.method == 'POST':
        data = request.data
        # Handle date conversion
        dob = data.get('dob')
        if dob and isinstance(dob, str):
            try:
                dob = datetime.strptime(dob, '%Y-%m-%d').date()
            except ValueError:
                dob = None
        
        order = Order.objects.create(
            patient_first_name=data.get('patient_first_name', ''),
            patient_last_name=data.get('patient_last_name', ''),
            dob=dob,
            status=data.get('status', 'new')
        )
        
        return Response({
            'id': order.id,
            'patient_first_name': order.patient_first_name,
            'patient_last_name': order.patient_last_name,
            'dob': order.dob.isoformat() if order.dob else None,
            'status': order.status,
            'created_at': order.created_at.isoformat(),
            'updated_at': order.updated_at.isoformat()
        }, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def order_detail(request, order_id):
    """Handle individual order operations"""
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        return Response({
            'id': order.id,
            'patient_first_name': order.patient_first_name,
            'patient_last_name': order.patient_last_name,
            'dob': order.dob.isoformat() if order.dob else None,
            'status': order.status,
            'created_at': order.created_at.isoformat(),
            'updated_at': order.updated_at.isoformat()
        })
    
    elif request.method == 'PUT':
        data = request.data
        # Handle date conversion
        dob = data.get('dob')
        if dob and isinstance(dob, str):
            try:
                dob = datetime.strptime(dob, '%Y-%m-%d').date()
            except ValueError:
                dob = order.dob  # Keep existing if invalid
        
        order.patient_first_name = data.get('patient_first_name', order.patient_first_name)
        order.patient_last_name = data.get('patient_last_name', order.patient_last_name)
        order.dob = dob if dob is not None else order.dob
        order.status = data.get('status', order.status)
        order.save()
        
        return Response({
            'id': order.id,
            'patient_first_name': order.patient_first_name,
            'patient_last_name': order.patient_last_name,
            'dob': order.dob.isoformat() if order.dob else None,
            'status': order.status,
            'created_at': order.created_at.isoformat(),
            'updated_at': order.updated_at.isoformat()
        })
    
    elif request.method == 'DELETE':
        order.delete()
        return Response({'message': 'Order deleted successfully'})
