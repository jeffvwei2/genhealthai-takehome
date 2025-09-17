#!/usr/bin/env python3
"""
Test script to verify the Patient Information Extraction System setup.
"""

import requests
import json
import os
import sys
from pathlib import Path

def test_backend_health():
    """Test if the backend is running and healthy."""
    try:
        response = requests.get('http://localhost:8001/api/upload/health/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Backend health check passed")
            print(f"   Response: {data}")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend not accessible: {e}")
        return False

def test_orders_api():
    """Test the orders API endpoints."""
    try:
        # Test GET orders
        response = requests.get('http://localhost:8001/api/orders/', timeout=5)
        if response.status_code == 200:
            print("✅ Orders API (GET) working")
        else:
            print(f"❌ Orders API (GET) failed: {response.status_code}")
            return False
        
        # Test POST order
        order_data = {
            'patient_first_name': 'Test',
            'patient_last_name': 'User',
            'dob': '1990-01-01',
            'status': 'new'
        }
        response = requests.post('http://localhost:8001/api/orders/', 
                               json=order_data, timeout=5)
        if response.status_code == 201:
            print("✅ Orders API (POST) working")
            order_id = response.json()['id']
            
            # Test DELETE order
            response = requests.delete(f'http://localhost:8001/api/orders/{order_id}/', timeout=5)
            if response.status_code == 200:
                print("✅ Orders API (DELETE) working")
                return True
            else:
                print(f"❌ Orders API (DELETE) failed: {response.status_code}")
                return False
        else:
            print(f"❌ Orders API (POST) failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Orders API test failed: {e}")
        return False

def test_pdf_upload():
    """Test PDF upload functionality."""
    try:
        # Check if test PDF exists
        pdf_path = Path('demopatient.pdf')
        if not pdf_path.exists():
            print("⚠️  Test PDF not found, skipping upload test")
            return True
        
        # Test PDF upload
        with open(pdf_path, 'rb') as f:
            files = {'file': f}
            response = requests.post('http://localhost:8001/api/upload/', 
                                   files=files, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ PDF upload working")
            print(f"   Extracted: {data.get('extracted', {})}")
            return True
        else:
            print(f"❌ PDF upload failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ PDF upload test failed: {e}")
        return False
    except FileNotFoundError:
        print("⚠️  Test PDF not found, skipping upload test")
        return True

def test_frontend():
    """Test if frontend is accessible."""
    try:
        response = requests.get('http://localhost:3000', timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is accessible")
            return True
        else:
            print(f"❌ Frontend not accessible: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Frontend not accessible: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Patient Information Extraction System Setup")
    print("=" * 60)
    
    tests = [
        ("Backend Health", test_backend_health),
        ("Orders API", test_orders_api),
        ("PDF Upload", test_pdf_upload),
        ("Frontend", test_frontend),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"   ❌ {test_name} test failed")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the setup.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
