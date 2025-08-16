"""
Simple test script for document parsing endpoint only
"""

import requests
import json
import os
from datetime import datetime

# Configuration
API_KEY = "2ZLp45FKyB9gVLLxeQGr6Om2qyAPltGI"
BASE_URL = "http://localhost:8000"

def test_parse_document():
    """Test the unified /parse-document endpoint"""
    
    print("🧪 Testing Document Parsing Endpoint...")
    
    # Check if test file exists
    test_file = "testing_doc/invalid_fw4.pdf"
    if not os.path.exists(test_file):
        print(f"❌ Test file '{test_file}' not found. Please ensure it exists.")
        return False
    
    try:
        with open(test_file, 'rb') as f:
            files = {'file': (test_file, f, 'application/pdf')}
            headers = {"X-API-Key": API_KEY}
            
            print(f"📤 Uploading: {test_file}")
            response = requests.post(
                f"{BASE_URL}/parse-document",
                files=files,
                headers=headers
            )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Document parsing successful!")
            
            print("\n📊 Document Analysis:")
            print(f"   • File: {result.get('filename')}")
            print(f"   • Size: {result.get('file_size_bytes', 0):,} bytes")
            print(f"   • Type: {result.get('document_metadata', {}).get('detected_document_type')}")
            print(f"   • Pages: {result.get('document_metadata', {}).get('total_pages')}")
            print(f"   • Content Blocks: {result.get('document_metadata', {}).get('total_content_blocks')}")
            
            if 'processing_instructions_for_llm' in result:
                instructions = result['processing_instructions_for_llm']
                print(f"   • LLM Approach: {instructions.get('suggested_approach')}")
            
            # Save results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            results_file = f'parsing_results_{timestamp}.json'
            with open(results_file, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\n💾 Results saved to: {results_file}")
            return True
            
        else:
            print(f"❌ Parsing failed with status code: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Make sure the server is running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Document Parsing\n")
    success = test_parse_document()
    
    if success:
        print("\n✨ Document parsing test completed successfully!")
    else:
        print("\n❌ Document parsing test failed!")