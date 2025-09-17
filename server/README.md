# Django PDF Processing Server

This is the Django backend for the PDF processing application.

## Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py migrate
```

3. Start the development server:
```bash
python manage.py runserver 8000
```

## API Endpoints

- `GET /api/test/` - Test endpoint
- `POST /api/upload/` - Upload and process PDF files
- `GET /api/orders/` - Get all orders
- `POST /api/orders/` - Create new order
- `DELETE /api/orders/{id}/` - Delete order

## Dependencies

- **Django**: Web framework
- **Django REST Framework**: API framework
- **django-cors-headers**: CORS support
- **pdfplumber**: PDF text extraction
- **pytesseract**: OCR for image-based PDFs
- **pdf2image**: Convert PDF to images for OCR
- **Pillow**: Image processing

## System Requirements

- Python 3.8+
- Tesseract OCR (install with `brew install tesseract` on macOS)
- Poppler (install with `brew install poppler` on macOS)
