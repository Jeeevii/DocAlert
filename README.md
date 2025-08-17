# Parserate Document Parsing Setup Guide

## 🔍 Overview

The Parserate document parsing feature uses Docling to extract and validate structured data from documents like PDFs, images, and forms. This helps automate HR document processing and reduces manual data entry errors.

## 📋 What It Does

- **Parses documents**: PDFs, images (PNG, JPG, TIFF, BMP)
- **Extracts structured data**: Names, SSNs, addresses, dates, etc.
- **Validates field formats**: Ensures data meets expected patterns
- **Template support**: Pre-configured templates for common forms
- **Auto-detection**: Can identify fields without templates
- **Validation reporting**: Shows what's missing or incorrect

## 🚀 Installation

### 1. Install Docling
```bash
cd backend
pip install docling
```

### 2. Update Requirements
The requirements.txt already includes docling. If you need to install manually:
```bash
pip install -r requirements.txt
```

### 3. Restart Server
```bash
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

## 🔧 API Endpoints

### 1. Parse Document
```
POST /parse-document
Headers: X-API-Key: your_api_key
Content-Type: multipart/form-data

Form Data:
- file: Document file (PDF, PNG, JPG, etc.)
- template_type: Optional (employment_form, tax_form, address_verification)
```

**Response Example:**
```json
{
  "success": true,
  "filename": "employment_form.pdf",
  "template_type": "employment_form",
  "page_count": 2,
  "fields": [
    {
      "page": 1,
      "title": "Employment Application Form",
      "question": "Full Name",
      "answer": "John Smith",
      "optional": false,
      "required": true,
      "field_type": "NAME",
      "format_expectation": ".*",
      "confidence": 0.8,
      "validation_status": "PASSED",
      "validation_errors": []
    }
  ],
  "validation_summary": {
    "total_fields": 5,
    "passed": 4,
    "failed": 1,
    "warnings": 0,
    "missing_required": 1,
    "validation_percentage": 80.0,
    "ready_for_processing": false
  }
}
```

### 2. Get Document Templates
```
GET /document-templates
Headers: X-API-Key: your_api_key
```

### 3. Validate Individual Field
```
POST /validate-document-field
Headers: X-API-Key: your_api_key
Content-Type: application/x-www-form-urlencoded

Form Data:
- field_type: SSN, EMAIL, PHONE, DATE, etc.
- field_value: Value to validate
```

## 📝 Supported Templates

### Employment Form
- Full Name (required)
- Social Security Number (required)
- Address (required)
- Phone Number (required)
- Email Address (required)
- Emergency Contact (optional)
- Previous Employer (optional)

### Tax Form
- SSN (required)
- Filing Status (required)
- Income (required)

### Address Verification
- Street Address (required)
- City (required)
- State (required)
- ZIP Code (required)

## 🔍 Supported Field Types

- **TEXT**: General text fields
- **SSN**: Social Security Numbers (XXX-XX-XXXX)
- **DATE**: Dates (MM/DD/YYYY or YYYY-MM-DD)
- **EMAIL**: Email addresses
- **PHONE**: Phone numbers (+1-XXX-XXX-XXXX)
- **ADDRESS_***: Street, City, State, ZIP
- **SIGNATURE**: Signature fields
- **CHECKBOX**: Checkbox values
- **NUMBER**: Numeric values
- **CURRENCY**: Currency amounts
- **NAME**: Person names

## 🧪 Testing

Run the document parsing test:
```bash
python test_document_parsing.py
```

This will test:
1. Health check and availability
2. Template retrieval
3. Field validation
4. Document parsing with sample data

## 💡 Usage Examples

### 1. Basic Document Parsing
```python
import requests

files = {"file": open("employment_form.pdf", "rb")}
headers = {"X-API-Key": "your_api_key"}
data = {"template_type": "employment_form"}

response = requests.post(
    "http://localhost:8000/parse-document",
    files=files,
    data=data,
    headers=headers
)

result = response.json()
print(f"Validation: {result['validation_summary']['ready_for_processing']}")
```

### 2. Field Validation
```python
response = requests.post(
    "http://localhost:8000/validate-document-field",
    data={
        "field_type": "SSN",
        "field_value": "123-45-6789"
    },
    headers={"X-API-Key": "your_api_key"}
)

print(f"Valid: {response.json()['is_valid']}")
```

## 🔗 Integration with Cortex.ai

Add document parsing to your Cortex.ai workflow:

```
Endpoint: https://your-app.onrender.com/parse-document
Method: POST (Multipart Form)
Headers: X-API-Key: your_api_key
Form Fields: 
- file: Document file
- template_type: employment_form (or other template)
```

## 🎯 Benefits for HR Processing

1. **Automated Data Extraction**: No manual typing from forms
2. **Format Validation**: Catches errors before processing
3. **Completeness Check**: Identifies missing required fields
4. **Quality Assurance**: Reduces data entry errors
5. **Processing Ready**: Clear indication when documents are complete
6. **Template Flexibility**: Supports various document types

## 📊 Validation Statuses

- **PASSED**: Field is valid and properly formatted
- **FAILED**: Field has validation errors (wrong format, etc.)
- **WARNING**: Field is missing but optional
- **PENDING**: Field not yet validated

## 🚨 Troubleshooting

### Document parsing not available
- Install docling: `pip install docling`
- Restart the server
- Check health endpoint: `/health`

### Low confidence scores
- Use higher quality scans
- Ensure text is clearly readable
- Consider using appropriate templates

### Validation failures
- Check field format expectations
- Use `/validate-document-field` to test individual values
- Review validation error messages

## 🔮 Future Enhancements

- Custom template creation
- Machine learning for better field detection
- Batch document processing
- Integration with external validation services
- Advanced OCR for handwritten text

Your DocAlert system now has powerful document parsing capabilities! 🎉
