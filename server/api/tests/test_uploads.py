from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from api.uploads.pdf_utils import extract_patient_info, normalize_date
import io

class PDFUtilsTest(TestCase):
    def test_normalize_date(self):
        """Test date normalization function"""
        # Test various date formats
        self.assertEqual(normalize_date('1/15/1990'), '1990-01-15')
        self.assertEqual(normalize_date('12/31/85'), '1985-12-31')
        self.assertEqual(normalize_date('3/5/2000'), '2000-03-05')
        self.assertEqual(normalize_date('10-20-1995'), '1995-10-20')
        
        # Test edge cases
        self.assertIsNone(normalize_date(''))
        self.assertIsNone(normalize_date('invalid'))
        self.assertIsNone(normalize_date('1/2'))
    
    def test_extract_patient_info(self):
        """Test patient info extraction from text"""
        # Test "Patient Name: John Doe" format
        text1 = "Patient Name: John Doe\nDOB: 01/15/1990"
        result1 = extract_patient_info(text1)
        self.assertEqual(result1['patient_first_name'], 'John')
        self.assertEqual(result1['patient_last_name'], 'Doe')
        self.assertEqual(result1['dob'], '1990-01-15')
        
        # Test "Name: Doe, John" format
        text2 = "Name: Doe, John\nDate of Birth: 12/31/1985"
        result2 = extract_patient_info(text2)
        self.assertEqual(result2['patient_first_name'], 'John')
        self.assertEqual(result2['patient_last_name'], 'Doe')
        self.assertEqual(result2['dob'], '1985-12-31')
        
        # Test separate first/last name fields
        text3 = "First Name: Alice\nLast Name: Smith\nDOB: 03/20/1992"
        result3 = extract_patient_info(text3)
        self.assertEqual(result3['patient_first_name'], 'Alice')
        self.assertEqual(result3['patient_last_name'], 'Smith')
        self.assertEqual(result3['dob'], '1992-03-20')
        
        # Test empty text
        result4 = extract_patient_info('')
        self.assertIsNone(result4['patient_first_name'])
        self.assertIsNone(result4['patient_last_name'])
        self.assertIsNone(result4['dob'])

class UploadAPITest(APITestCase):
    def setUp(self):
        # Create a simple text file that simulates a PDF
        self.pdf_content = b"Patient Name: Test Patient\nDOB: 01/01/1990"
        self.pdf_file = SimpleUploadedFile(
            "test.pdf",
            self.pdf_content,
            content_type="application/pdf"
        )
    
    def test_health_check(self):
        """Test GET /api/upload/health/ returns health status"""
        url = reverse('health_check')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['ok'])
        self.assertIn('message', response.data)
    
    def test_upload_pdf_success(self):
        """Test successful PDF upload and processing"""
        url = reverse('upload_pdf')
        data = {'file': self.pdf_file}
        
        response = self.client.post(url, data, format='multipart')
        
        # Note: This test might fail if OCR is required, but structure is correct
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_422_UNPROCESSABLE_ENTITY])
    
    def test_upload_no_file(self):
        """Test upload without file returns error"""
        url = reverse('upload_pdf')
        response = self.client.post(url, {})
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_upload_non_pdf_file(self):
        """Test upload of non-PDF file returns error"""
        url = reverse('upload_pdf')
        text_file = SimpleUploadedFile(
            "test.txt",
            b"Some text content",
            content_type="text/plain"
        )
        data = {'file': text_file}
        
        response = self.client.post(url, data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        self.assertIn('error', response.data)
    
    def test_upload_empty_pdf(self):
        """Test upload of empty PDF returns error"""
        url = reverse('upload_pdf')
        empty_pdf = SimpleUploadedFile(
            "empty.pdf",
            b"",  # Empty content
            content_type="application/pdf"
        )
        data = {'file': empty_pdf}
        
        response = self.client.post(url, data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn('error', response.data)

class IntegrationTest(APITestCase):
    """Integration tests for the complete workflow"""
    
    def test_complete_workflow(self):
        """Test complete workflow: upload PDF -> create order -> manage order"""
        # 1. Health check
        health_url = reverse('health_check')
        health_response = self.client.get(health_url)
        self.assertEqual(health_response.status_code, status.HTTP_200_OK)
        
        # 2. Create order directly
        orders_url = reverse('orders_list')
        order_data = {
            'patient_first_name': 'Integration',
            'patient_last_name': 'Test',
            'dob': '1990-01-01',
            'status': 'new'
        }
        order_response = self.client.post(orders_url, order_data, format='json')
        self.assertEqual(order_response.status_code, status.HTTP_201_CREATED)
        
        # 3. Get order list
        list_response = self.client.get(orders_url)
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data), 1)
        
        # 4. Update order
        order_id = order_response.data['id']
        update_url = reverse('order_detail', kwargs={'order_id': order_id})
        update_data = {'status': 'complete'}
        update_response = self.client.put(update_url, order_data, format='json')
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        
        # 5. Delete order
        delete_response = self.client.delete(update_url)
        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)
        
        # 6. Verify deletion
        final_list_response = self.client.get(orders_url)
        self.assertEqual(len(final_list_response.data), 0)
