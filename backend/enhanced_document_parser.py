"""
Enhanced Document Parser for LLM Processing
Extracts comprehensive document structure for intelligent parsing by LLMs
"""

import os
import tempfile
from typing import List, Dict, Any, Optional
import re
from pathlib import Path

# Import the simple parser as base
try:
    import pypdf as PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    from PIL import Image
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

class EnhancedDocumentParser:
    """Enhanced parser that extracts comprehensive document structure for LLM processing."""
    
    def __init__(self):
        self.pdf_available = PDF_AVAILABLE
        self.ocr_available = OCR_AVAILABLE
        print(f"Enhanced Parser initialized - PDF: {self.pdf_available}, OCR: {self.ocr_available}")
    
    async def parse_document_for_llm(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """
        Parse document and return comprehensive structure for LLM processing.
        
        Returns a format optimized for LLM understanding with:
        - Document metadata
        - Page-by-page content
        - Text blocks and their positions
        - Detected patterns and structures
        - Raw text for analysis
        """
        try:
            file_extension = Path(filename).suffix.lower()
            
            # Extract text and structure based on file type
            if file_extension == '.pdf':
                if not self.pdf_available:
                    return self._error_response("PDF processing not available. Install pypdf.", filename)
                document_data = self._extract_pdf_structure(file_content)
            elif file_extension in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
                if not self.ocr_available:
                    return self._error_response("OCR not available. Install PIL and pytesseract.", filename)
                document_data = self._extract_image_structure(file_content)
            else:
                return self._error_response(f"Unsupported file type: {file_extension}", filename)
            
            if not document_data:
                return self._error_response("Could not extract content from document", filename)
            
            # Enhance with analysis
            enhanced_data = self._enhance_with_analysis(document_data)
            
            # Create final LLM-optimized format
            return {
                "success": True,
                "filename": filename,
                "file_type": file_extension,
                "file_size_bytes": len(file_content),
                "extraction_method": "pdf" if file_extension == '.pdf' else "ocr",
                "document_metadata": enhanced_data["metadata"],
                "pages": enhanced_data["pages"],
                "document_structure": enhanced_data["structure"],
                "extracted_patterns": enhanced_data["patterns"],
                "processing_instructions_for_llm": {
                    "suggested_approach": "Analyze each page's content blocks to identify form fields, questions, and answers",
                    "key_areas_to_focus": ["labeled_fields", "checkbox_patterns", "signature_areas", "date_fields", "structured_sections"],
                    "confidence_scoring": "Use text_confidence and pattern_matches for reliability assessment",
                    "next_steps": "Parse content_blocks to extract question-answer pairs and validate against common form patterns"
                }
            }
            
        except Exception as e:
            return self._error_response(f"Document parsing error: {str(e)}", filename)
    
    def _extract_pdf_structure(self, file_content: bytes) -> Optional[Dict]:
        """Extract comprehensive structure from PDF."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(file_content)
            tmp_file_path = tmp_file.name
        
        try:
            pages_data = []
            
            with open(tmp_file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                for page_num, page in enumerate(reader.pages, 1):
                    # Extract text
                    page_text = page.extract_text()
                    
                    # Split into lines and analyze structure
                    lines = [line.strip() for line in page_text.split('\n') if line.strip()]
                    
                    # Analyze content blocks
                    content_blocks = self._analyze_text_blocks(lines)
                    
                    # Try to get page dimensions if available
                    try:
                        media_box = page.mediabox
                        page_width = float(media_box.width)
                        page_height = float(media_box.height)
                    except:
                        page_width = 612  # Default letter size
                        page_height = 792
                    
                    page_data = {
                        "page_number": page_num,
                        "page_dimensions": {
                            "width": page_width,
                            "height": page_height
                        },
                        "raw_text": page_text,
                        "text_lines": lines,
                        "content_blocks": content_blocks,
                        "text_confidence": 0.9,  # PDF text extraction is usually reliable
                        "extraction_notes": "Direct PDF text extraction"
                    }
                    
                    pages_data.append(page_data)
                
                return {
                    "metadata": {
                        "total_pages": len(pages_data),
                        "extraction_method": "pdf_direct",
                        "has_embedded_text": True
                    },
                    "pages": pages_data
                }
        
        finally:
            os.unlink(tmp_file_path)
    
    def _extract_image_structure(self, file_content: bytes) -> Optional[Dict]:
        """Extract structure from image using OCR."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
            tmp_file.write(file_content)
            tmp_file_path = tmp_file.name
        
        try:
            image = Image.open(tmp_file_path)
            
            # Get image dimensions
            width, height = image.size
            
            # Extract text with OCR
            text = pytesseract.image_to_string(image)
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            
            # Analyze content blocks
            content_blocks = self._analyze_text_blocks(lines)
            
            page_data = {
                "page_number": 1,
                "page_dimensions": {
                    "width": width,
                    "height": height
                },
                "raw_text": text,
                "text_lines": lines,
                "content_blocks": content_blocks,
                "text_confidence": 0.7,  # OCR is less reliable
                "extraction_notes": "OCR text extraction from image"
            }
            
            return {
                "metadata": {
                    "total_pages": 1,
                    "extraction_method": "ocr",
                    "has_embedded_text": False
                },
                "pages": [page_data]
            }
        
        finally:
            os.unlink(tmp_file_path)
    
    def _analyze_text_blocks(self, lines: List[str]) -> List[Dict]:
        """Analyze text lines and group into meaningful content blocks."""
        content_blocks = []
        current_block = []
        block_type = "text"
        
        for i, line in enumerate(lines):
            # Detect different types of content
            line_type = self._classify_line(line)
            
            # Start new block if type changes or if it's a clear separator
            if (line_type != block_type and current_block) or self._is_separator_line(line):
                if current_block:
                    content_blocks.append({
                        "block_id": len(content_blocks) + 1,
                        "block_type": block_type,
                        "content": current_block.copy(),
                        "combined_text": " ".join(current_block),
                        "line_range": {
                            "start": i - len(current_block),
                            "end": i - 1
                        },
                        "patterns_detected": self._detect_patterns_in_block(current_block)
                    })
                current_block = []
                block_type = line_type
            
            if not self._is_separator_line(line):
                current_block.append(line)
        
        # Add final block
        if current_block:
            content_blocks.append({
                "block_id": len(content_blocks) + 1,
                "block_type": block_type,
                "content": current_block.copy(),
                "combined_text": " ".join(current_block),
                "line_range": {
                    "start": len(lines) - len(current_block),
                    "end": len(lines) - 1
                },
                "patterns_detected": self._detect_patterns_in_block(current_block)
            })
        
        return content_blocks
    
    def _classify_line(self, line: str) -> str:
        """Classify a line of text by its apparent purpose."""
        line_lower = line.lower().strip()
        
        # Title/Header patterns
        if (line.isupper() and len(line) > 5) or any(word in line_lower for word in ['form', 'application', 'document', 'certificate']):
            return "title"
        
        # Field label patterns
        if any(char in line for char in [':', '_', '□', '☐', '☑', '☒']) or line.endswith(':'):
            return "field_label"
        
        # Instruction patterns
        if any(word in line_lower for word in ['enter', 'fill', 'complete', 'sign', 'date', 'print', 'check']):
            return "instruction"
        
        # Section header patterns
        if line.endswith(':') or (len(line) < 50 and not any(char in line for char in ['.', ',', ';'])):
            return "section_header"
        
        return "text"
    
    def _is_separator_line(self, line: str) -> bool:
        """Check if a line is likely a separator."""
        # Lines with mostly special characters
        special_chars = set('-_=*#|+')
        if len(line) > 3 and len(set(line) & special_chars) / len(set(line)) > 0.7:
            return True
        
        # Very short lines that might be separators
        if len(line.strip()) < 3:
            return True
        
        return False
    
    def _detect_patterns_in_block(self, block_lines: List[str]) -> Dict[str, Any]:
        """Detect common patterns within a content block."""
        combined_text = " ".join(block_lines)
        patterns = {
            "contains_ssn": bool(re.search(r'\d{3}-?\d{2}-?\d{4}', combined_text)),
            "contains_date": bool(re.search(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', combined_text)),
            "contains_phone": bool(re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', combined_text)),
            "contains_email": bool(re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', combined_text)),
            "contains_checkbox": any('□' in line or '☐' in line or '☑' in line or '☒' in line for line in block_lines),
            "contains_underscores": any('_' in line for line in block_lines),
            "has_colon_separator": any(':' in line for line in block_lines),
            "line_count": len(block_lines),
            "avg_line_length": sum(len(line) for line in block_lines) / len(block_lines) if block_lines else 0,
            "contains_signature_area": any(word in combined_text.lower() for word in ['signature', 'sign', 'signed']),
            "contains_dollar_amounts": bool(re.search(r'\$\d+', combined_text)),
            "appears_to_be_form_field": bool(re.search(r':\s*_{3,}|_{5,}', combined_text))
        }
        
        return patterns
    
    def _enhance_with_analysis(self, document_data: Dict) -> Dict:
        """Enhance document data with higher-level analysis."""
        pages = document_data["pages"]
        
        # Document-level analysis
        total_blocks = sum(len(page["content_blocks"]) for page in pages)
        
        # Detect document type based on content
        all_text = " ".join(page["raw_text"] for page in pages).lower()
        document_type = self._detect_document_type(all_text)
        
        # Find key patterns across all pages
        global_patterns = self._detect_global_patterns(pages)
        
        # Identify likely form structure
        form_structure = self._analyze_form_structure(pages)
        
        enhanced_data = {
            "metadata": {
                **document_data["metadata"],
                "detected_document_type": document_type,
                "total_content_blocks": total_blocks,
                "analysis_timestamp": "auto",
                "complexity_score": self._calculate_complexity_score(pages)
            },
            "pages": pages,
            "structure": {
                "form_structure": form_structure,
                "section_hierarchy": self._build_section_hierarchy(pages),
                "field_distribution": self._analyze_field_distribution(pages)
            },
            "patterns": global_patterns
        }
        
        return enhanced_data
    
    def _detect_document_type(self, text: str) -> str:
        """Detect the type of document based on content."""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['w-4', 'w4', 'employee withholding', 'allowances']):
            return "tax_form_w4"
        elif any(word in text_lower for word in ['employment', 'application', 'job', 'position']):
            return "employment_application"
        elif any(word in text_lower for word in ['i-9', 'employment eligibility', 'citizenship']):
            return "employment_verification_i9"
        elif any(word in text_lower for word in ['address', 'verification', 'residence']):
            return "address_verification"
        elif any(word in text_lower for word in ['tax', 'return', '1040', 'irs']):
            return "tax_document"
        elif any(word in text_lower for word in ['invoice', 'bill', 'payment', 'due']):
            return "financial_document"
        else:
            return "general_form"
    
    def _detect_global_patterns(self, pages: List[Dict]) -> Dict:
        """Detect patterns that span across the entire document."""
        all_blocks = []
        for page in pages:
            all_blocks.extend(page["content_blocks"])
        
        # Count pattern occurrences
        total_checkboxes = sum(1 for block in all_blocks if block["patterns_detected"]["contains_checkbox"])
        total_signature_areas = sum(1 for block in all_blocks if block["patterns_detected"]["contains_signature_area"])
        total_form_fields = sum(1 for block in all_blocks if block["patterns_detected"]["appears_to_be_form_field"])
        
        return {
            "checkbox_count": total_checkboxes,
            "signature_areas": total_signature_areas,
            "form_fields_detected": total_form_fields,
            "has_structured_layout": total_form_fields > 3,
            "document_complexity": "high" if total_form_fields > 10 else "medium" if total_form_fields > 5 else "low",
            "primary_content_types": self._get_primary_content_types(all_blocks)
        }
    
    def _analyze_form_structure(self, pages: List[Dict]) -> Dict:
        """Analyze the overall form structure."""
        sections = []
        current_section = None
        
        for page in pages:
            for block in page["content_blocks"]:
                if block["block_type"] == "section_header":
                    if current_section:
                        sections.append(current_section)
                    current_section = {
                        "section_title": block["combined_text"],
                        "page": page["page_number"],
                        "fields": []
                    }
                elif block["block_type"] == "field_label" and current_section:
                    current_section["fields"].append(block["combined_text"])
        
        if current_section:
            sections.append(current_section)
        
        return {
            "sections": sections,
            "section_count": len(sections),
            "appears_multi_section": len(sections) > 1
        }
    
    def _build_section_hierarchy(self, pages: List[Dict]) -> List[Dict]:
        """Build a hierarchy of document sections."""
        hierarchy = []
        
        for page in pages:
            page_sections = []
            for block in page["content_blocks"]:
                if block["block_type"] in ["title", "section_header"]:
                    page_sections.append({
                        "type": block["block_type"],
                        "text": block["combined_text"],
                        "block_id": block["block_id"]
                    })
            
            if page_sections:
                hierarchy.append({
                    "page": page["page_number"],
                    "sections": page_sections
                })
        
        return hierarchy
    
    def _analyze_field_distribution(self, pages: List[Dict]) -> Dict:
        """Analyze how fields are distributed across pages."""
        field_counts = {}
        
        for page in pages:
            page_num = page["page_number"]
            field_count = sum(1 for block in page["content_blocks"] 
                            if block["block_type"] == "field_label" or 
                               block["patterns_detected"]["appears_to_be_form_field"])
            field_counts[f"page_{page_num}"] = field_count
        
        return {
            "fields_per_page": field_counts,
            "total_fields": sum(field_counts.values()),
            "most_dense_page": max(field_counts.items(), key=lambda x: x[1])[0] if field_counts else None
        }
    
    def _get_primary_content_types(self, blocks: List[Dict]) -> List[str]:
        """Get the primary types of content in the document."""
        type_counts = {}
        for block in blocks:
            block_type = block["block_type"]
            type_counts[block_type] = type_counts.get(block_type, 0) + 1
        
        # Return types sorted by frequency
        return sorted(type_counts.keys(), key=lambda x: type_counts[x], reverse=True)
    
    def _calculate_complexity_score(self, pages: List[Dict]) -> float:
        """Calculate a complexity score for the document."""
        total_blocks = sum(len(page["content_blocks"]) for page in pages)
        total_lines = sum(len(page["text_lines"]) for page in pages)
        
        # Simple complexity calculation
        if total_blocks == 0:
            return 0.0
        
        avg_blocks_per_page = total_blocks / len(pages)
        avg_lines_per_block = total_lines / total_blocks if total_blocks > 0 else 0
        
        # Normalize to 0-1 scale
        complexity = min(1.0, (avg_blocks_per_page * 0.1) + (avg_lines_per_block * 0.05))
        return round(complexity, 2)
    
    def _error_response(self, error_msg: str, filename: str) -> Dict:
        """Create standardized error response."""
        return {
            "success": False,
            "error": error_msg,
            "filename": filename,
            "document_metadata": None,
            "pages": [],
            "document_structure": None,
            "extracted_patterns": None
        }
