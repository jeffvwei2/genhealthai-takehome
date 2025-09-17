# Patient Information Extraction System

A full-stack application for extracting patient information from PDF documents using OCR and text extraction.

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **Tesseract OCR**
- **Poppler** (for PDF to image conversion)

### Installation

1. **Clone the repository**

2. **Install system dependencies**
   
   **macOS (with Homebrew):**
   ```bash
   brew install tesseract poppler
   ```

3. **Start the application**
   
   Create a .env file in /server repository as outlined in the Configuration section below
   
   ```bash
   ./start.sh
   ```

   This script will:
   - Set up Python virtual environment
   - Install Python dependencies
   - Run Django migrations
   - Start Django server on port 8001
   - Install Node.js dependencies
   - Start React development server on port 3000

5. **Access the application**
   - **Frontend**: http://localhost:3000
   - **Backend API**: http://localhost:8001

## 🔧 Manual Setup (Alternative)

If the automated script doesn't work, you can set up manually:

### Backend Setup
```bash
cd server
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8001
```

### Frontend Setup
```bash
cd client
npm install
npm run dev
```

## ⚙️ Configuration

### Environment Variables

The `.env` file in the `server/` directory contains:

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=sqlite:///db.sqlite3

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
CORS_ALLOW_ALL_ORIGINS=True

# Tesseract OCR (update path for your system)
TESSERACT_CMD=/opt/homebrew/bin/tesseract

# Server Port
SERVER_PORT=8001
```

### Tesseract Path Configuration

Update `TESSERACT_CMD` in your `.env` file if needed:

- **macOS (Homebrew)**: `/opt/homebrew/bin/tesseract`
- **Ubuntu/Debian**: `/usr/bin/tesseract`
- **Windows**: `C:\Program Files\Tesseract-OCR\tesseract.exe`

## 🧪 Testing

Run the test suite:

```bash
cd server
source venv/bin/activate
python manage.py test
```

## 📚 API Endpoints

### Orders API
- `GET /api/orders/` - List all patient orders
- `POST /api/orders/` - Create new order
- `GET /api/orders/{id}/` - Get specific order
- `PUT /api/orders/{id}/` - Update order
- `DELETE /api/orders/{id}/` - Delete order

### Upload API
- `GET /api/upload/health/` - Health check
- `POST /api/upload/` - Upload and process PDF

## 🔍 Features

- **PDF Text Extraction**: Direct text extraction using `pdfplumber`
- **OCR Processing**: Tesseract OCR for image-based PDFs
- **Patient Information Parsing**: Extracts first name, last name, and DOB
- **Modern React Frontend**: simple UI
- **RESTful API**: Django REST Framework
- **Comprehensive Testing**: Unit and integration tests

## 📝 Usage

1. **Upload a PDF**: Use the upload form to select and upload a PDF file
2. **View Results**: Patient information will be automatically extracted and displayed
3. **Manage Orders**: View, edit, or delete patient orders
4. **Test with Sample**: Use the included `demopatient.pdf` for testing


## 📄 License

This project is licensed under the MIT License.
