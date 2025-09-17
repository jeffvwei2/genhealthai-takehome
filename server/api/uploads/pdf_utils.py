import pdfplumber
import pytesseract
from pdf2image import convert_from_bytes
import re
from django.conf import settings

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD

def normalize_date(date_str):
    """Normalize date string to YYYY-MM-DD format"""
    if not date_str:
        return None
    
    # Replace dashes with slashes for consistent parsing
    date_str = date_str.replace('-', '/')
    parts = date_str.split('/')
    
    if len(parts) != 3:
        return None
    
    month, day, year = parts
    
    # Handle 2-digit years
    if len(year) == 2:
        year_num = int(year)
        if year_num >= 70:
            year = f"19{year}"
        else:
            year = f"20{year}"
    
    # Pad with zeros
    month = month.zfill(2)
    day = day.zfill(2)
    
    return f"{year}-{month}-{day}"

def extract_text_from_pdf(pdf_file):
    """Extract text from PDF using pdfplumber first, then OCR if needed"""
    text = ""
    
    # Try pdfplumber first
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"pdfplumber failed: {e}")
    
    # If no text extracted, try OCR
    if not text or len(text.strip()) < 10:
        try:
            # Reset file pointer
            pdf_file.seek(0)
            pdf_bytes = pdf_file.read()
            
            # Convert PDF to images
            images = convert_from_bytes(pdf_bytes, dpi=200)
            
            for image in images:
                # Use pytesseract for OCR
                page_text = pytesseract.image_to_string(image, config='--psm 6')
                if page_text:
                    text += page_text + "\n"
                    
        except Exception as e:
            print(f"OCR failed: {e}")
    
    return text

def extract_patient_info(text):
    """Extract patient information from text"""
    if not text:
        return {
            'patient_first_name': None,
            'patient_last_name': None,
            'dob': None
        }
    
    first_name = None
    last_name = None
    dob = None
    
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Look for "Patient Name: John Doe" or "Name: John Doe"
        name_match = re.search(r'\b(?:Patient Name|Name)\b\s*:\s*([A-Za-z][A-Za-z\-\']*)\s+([A-Za-z][A-Za-z\-\']*)', line, re.IGNORECASE)
        if name_match:
            first_name = name_match.group(1)
            last_name = name_match.group(2)
        
        # Look for "Patient Name: Doe, John" or "Name: Doe, John"
        comma_match = re.search(r'\b(?:Patient Name|Name)\b\s*:\s*([A-Za-z][A-Za-z\-\']*)\s*,\s*([A-Za-z][A-Za-z\-\']*)', line, re.IGNORECASE)
        if comma_match:
            last_name = comma_match.group(1)
            first_name = comma_match.group(2)
        
        # Look for separate "First Name: John" patterns
        first_match = re.search(r'\b(?:First Name|Given Name|First)\b\s*:\s*([A-Za-z][A-Za-z\-\']*)', line, re.IGNORECASE)
        if first_match and not first_name:
            first_name = first_match.group(1)
        
        # Look for separate "Last Name: Doe" patterns
        last_match = re.search(r'\b(?:Last Name|Family Name|Surname|Last)\b\s*:\s*([A-Za-z][A-Za-z\-\']*)', line, re.IGNORECASE)
        if last_match and not last_name:
            last_name = last_match.group(1)
        
        # Look for DOB patterns
        dob_match = re.search(r'\b(?:DOB|Date of Birth)\b\s*:\s*(\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4})', line, re.IGNORECASE)
        if dob_match:
            dob = normalize_date(dob_match.group(1))
    
    return {
        'patient_first_name': first_name,
        'patient_last_name': last_name,
        'dob': dob
    }
