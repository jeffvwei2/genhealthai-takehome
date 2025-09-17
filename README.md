# Patient Information Extraction System

A full-stack application for extracting patient information from PDF documents using OCR and text extraction.

## 🏗️ Project Structure

```
test-proj/
├── client/                 # React frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── UploadPDF.jsx    # PDF upload component
│   │   │   ├── Orders.jsx       # Patient orders management
│   │   │   └── FetchDisplay.jsx # Data display component
│   │   └── App.jsx
│   └── package.json
├── server/                 # Django backend
│   ├── api/
│   │   ├── orders/         # Orders app
│   │   │   ├── models.py   # Order model
│   │   │   ├── views.py    # Order views
│   │   │   └── urls.py     # Order URLs
│   │   ├── uploads/        # Uploads app
│   │   │   ├── views.py    # Upload views
│   │   │   ├── pdf_utils.py # PDF processing utilities
│   │   │   └── urls.py     # Upload URLs
│   │   └── tests/          # Test suite
│   ├── django_backend/
│   │   └── settings.py     # Django settings
│   ├── .env                # Environment variables
│   ├── env.example         # Environment variables template
│   └── requirements.txt    # Python dependencies
├── .gitignore             # Git ignore rules
└── demopatient.pdf        # Test PDF file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Tesseract OCR
- Poppler (for PDF to image conversion)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd test-proj
   ```

2. **Install system dependencies**
   ```bash
   # macOS with Homebrew
   brew install tesseract poppler
   
   # Ubuntu/Debian
   sudo apt-get install tesseract-ocr poppler-utils
   
   # Windows
   # Download and install Tesseract and Poppler from their official websites
   ```

3. **Backend Setup**
   ```bash
   cd server
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp env.example .env
   # Edit .env with your configuration
   python manage.py migrate
   python manage.py runserver 8001
   ```

4. **Frontend Setup**
   ```bash
   cd client
   npm install
   npm run dev
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8001

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `server/` directory based on `env.example`:

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=sqlite:///db.sqlite3

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
CORS_ALLOW_ALL_ORIGINS=True

# Tesseract OCR
TESSERACT_CMD=/opt/homebrew/bin/tesseract

# Server Port
SERVER_PORT=8001

# Development
ENVIRONMENT=development
```

### Tesseract Configuration

Update the `TESSERACT_CMD` in your `.env` file based on your system:

- **macOS (Homebrew)**: `/opt/homebrew/bin/tesseract`
- **Ubuntu/Debian**: `/usr/bin/tesseract`
- **Windows**: `C:\Program Files\Tesseract-OCR\tesseract.exe`

## 📚 API Endpoints

### Orders API
- `GET /api/orders/` - List all orders
- `POST /api/orders/` - Create new order
- `GET /api/orders/{id}/` - Get specific order
- `PUT /api/orders/{id}/` - Update order
- `DELETE /api/orders/{id}/` - Delete order

### Upload API
- `GET /api/upload/health/` - Health check
- `POST /api/upload/` - Upload and process PDF

## 🧪 Testing

Run the test suite:

```bash
cd server
source venv/bin/activate
python manage.py test
```

## 🔍 Features

- **PDF Text Extraction**: Uses `pdfplumber` for direct text extraction
- **OCR Processing**: Falls back to Tesseract OCR for image-based PDFs
- **Patient Information Parsing**: Extracts first name, last name, and DOB
- **RESTful API**: Django REST Framework for API endpoints
- **CORS Support**: Configured for frontend-backend communication
- **Environment Configuration**: Secure environment variable management
- **Comprehensive Testing**: Unit and integration tests

## 🛠️ Development

### Adding New Features

1. **New API Endpoints**: Add to appropriate app (`orders/` or `uploads/`)
2. **New Models**: Create in `api/orders/models.py`
3. **New Tests**: Add to `api/tests/`

### Code Organization

- **Orders App**: Handles patient order CRUD operations
- **Uploads App**: Handles PDF upload and processing
- **Tests**: Organized by functionality in `api/tests/`

## 🚀 Deployment

### Production Settings

1. Set `DEBUG=False` in `.env`
2. Generate a secure `SECRET_KEY`
3. Configure proper `ALLOWED_HOSTS`
4. Set up a production database
5. Configure static file serving
6. Set up proper CORS origins

### Docker (Optional)

```dockerfile
# Example Dockerfile for production
FROM python:3.11-slim
WORKDIR /app
COPY server/requirements.txt .
RUN pip install -r requirements.txt
COPY server/ .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
```

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📞 Support

For issues and questions, please open an issue in the repository.