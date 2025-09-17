#!/bin/bash

# Patient Information Extraction System Startup Script

echo "🚀 Starting Patient Information Extraction System..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ and try again."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ and try again."
    exit 1
fi

# Check if Tesseract is installed
if ! command -v tesseract &> /dev/null; then
    echo "❌ Tesseract OCR is not installed. Please install Tesseract and try again."
    echo "   macOS: brew install tesseract"
    echo "   Ubuntu: sudo apt-get install tesseract-ocr"
    exit 1
fi

# Check if Poppler is installed
if ! command -v pdftoppm &> /dev/null; then
    echo "❌ Poppler is not installed. Please install Poppler and try again."
    echo "   macOS: brew install poppler"
    echo "   Ubuntu: sudo apt-get install poppler-utils"
    exit 1
fi

echo "✅ All dependencies are installed."

# Start backend
echo "🔧 Starting Django backend..."
cd server

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "⚠️  Please edit server/.env with your configuration before running again."
    exit 1
fi

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate

# Start Django server in background
echo "🚀 Starting Django server on port 8001..."
python manage.py runserver 8001 &
DJANGO_PID=$!

# Wait for Django to start
sleep 5

# Start frontend
echo "🎨 Starting React frontend..."
cd ../client

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

# Start React development server
echo "🚀 Starting React development server on port 3000..."
npm run dev &
REACT_PID=$!

echo ""
echo "🎉 Application started successfully!"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8001"
echo ""
echo "Press Ctrl+C to stop both servers."

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $DJANGO_PID 2>/dev/null
    kill $REACT_PID 2>/dev/null
    echo "✅ Servers stopped."
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Wait for user to stop
wait
