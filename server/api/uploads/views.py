from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .pdf_utils import extract_text_from_pdf, extract_patient_info

@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    return Response({'ok': True, 'message': 'API is working'})

@api_view(['POST'])
def upload_pdf(request):
    """Upload and process PDF file"""
    if not request.FILES.get('file'):
        return Response({'error': 'file is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    pdf_file = request.FILES['file']
    
    # Check file type
    if not pdf_file.name.lower().endswith('.pdf'):
        return Response({'error': 'Unsupported file type. Please upload a PDF.'}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    
    try:
        # Extract text from PDF
        text = extract_text_from_pdf(pdf_file)
        
        if not text or len(text.strip()) < 10:
            return Response({'error': 'No extractable text found in PDF'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        # Extract patient information
        extracted = extract_patient_info(text)
        
        if not extracted['patient_first_name'] and not extracted['patient_last_name'] and not extracted['dob']:
            return Response({'error': 'Could not extract patient info from PDF'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        return Response({'extracted': extracted})
        
    except Exception as e:
        return Response({'error': 'Failed to process PDF', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)
