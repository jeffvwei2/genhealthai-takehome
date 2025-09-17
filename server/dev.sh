#!/bin/bash

# Django Development Server Startup Script

echo "🔧 Starting Django Development Server..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    echo "   Run: python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please create one from env.example"
    echo "   Run: cp env.example .env"
    exit 1
fi

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate

# Run tests
echo "🧪 Running tests..."
python manage.py test

# Start development server
echo "🚀 Starting Django development server on port 8001..."
echo "   API Documentation: http://localhost:8001/api/"
echo "   Health Check: http://localhost:8001/api/upload/health/"
echo ""
echo "Press Ctrl+C to stop the server."

python manage.py runserver 8001
