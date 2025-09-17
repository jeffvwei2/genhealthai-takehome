from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from api.orders.models import Order
import json

class OrderModelTest(TestCase):
    def setUp(self):
        self.order = Order.objects.create(
            patient_first_name='John',
            patient_last_name='Doe',
            dob='1990-01-01',
            status='new'
        )
    
    def test_order_creation(self):
        """Test order model creation"""
        self.assertEqual(self.order.patient_first_name, 'John')
        self.assertEqual(self.order.patient_last_name, 'Doe')
        self.assertEqual(str(self.order), 'John Doe')
    
    def test_order_str_representation(self):
        """Test order string representation"""
        self.assertEqual(str(self.order), 'John Doe')

class OrdersAPITest(APITestCase):
    def setUp(self):
        self.order = Order.objects.create(
            patient_first_name='Jane',
            patient_last_name='Smith',
            dob='1985-05-15',
            status='processing'
        )
    
    def test_get_orders_list(self):
        """Test GET /api/orders/ returns list of orders"""
        url = reverse('orders_list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['patient_first_name'], 'Jane')
        self.assertEqual(response.data[0]['patient_last_name'], 'Smith')
    
    def test_create_order(self):
        """Test POST /api/orders/ creates new order"""
        url = reverse('orders_list')
        data = {
            'patient_first_name': 'Bob',
            'patient_last_name': 'Johnson',
            'dob': '1992-03-20',
            'status': 'new'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['patient_first_name'], 'Bob')
        self.assertEqual(response.data['patient_last_name'], 'Johnson')
        self.assertEqual(Order.objects.count(), 2)
    
    def test_create_order_minimal_data(self):
        """Test creating order with minimal required data"""
        url = reverse('orders_list')
        data = {
            'patient_first_name': 'Alice',
            'patient_last_name': 'Brown'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'new')  # Default status
    
    def test_get_order_detail(self):
        """Test GET /api/orders/{id}/ returns specific order"""
        url = reverse('order_detail', kwargs={'order_id': self.order.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['patient_first_name'], 'Jane')
        self.assertEqual(response.data['id'], self.order.id)
    
    def test_get_nonexistent_order(self):
        """Test GET /api/orders/{id}/ with non-existent order"""
        url = reverse('order_detail', kwargs={'order_id': 999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
    
    def test_update_order(self):
        """Test PUT /api/orders/{id}/ updates order"""
        url = reverse('order_detail', kwargs={'order_id': self.order.id})
        data = {
            'patient_first_name': 'Jane',
            'patient_last_name': 'Smith',
            'dob': '1985-05-15',
            'status': 'complete'
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'complete')
        
        # Verify in database
        updated_order = Order.objects.get(id=self.order.id)
        self.assertEqual(updated_order.status, 'complete')
    
    def test_delete_order(self):
        """Test DELETE /api/orders/{id}/ deletes order"""
        url = reverse('order_detail', kwargs={'order_id': self.order.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(Order.objects.count(), 0)
    
    def test_delete_nonexistent_order(self):
        """Test DELETE /api/orders/{id}/ with non-existent order"""
        url = reverse('order_detail', kwargs={'order_id': 999})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
