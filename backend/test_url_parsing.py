"""
Test script for the URL-based document parsing endpoint
"""

import requests
import json
from datetime import datetime

# Configuration
API_KEY = "2ZLp45FKyB9gVLLxeQGr6Om2qyAPltGI"
BASE_URL = "http://localhost:8000"

def test_parse_document_from_url():
    """Test the /parse-document endpoint with a file URL"""
    
    print("🧪 Testing URL-based Document Parsing...")
    
    # Test with a sample PDF URL - you can replace this with any publicly accessible PDF
    test_urls = [
        {
            "url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
            "description": "Sample PDF from W3C"
        },
        {
            "url": "https://www.adobe.com/support/products/enterprise/knowledgecenter/media/c4611_sample_explain.pdf",
            "description": "Adobe sample PDF"
        }
    ]
    
    for i, test_case in enumerate(test_urls, 1):
        print(f"\n--- Test {i}: {test_case['description']} ---")
        
        try:
            # Prepare request data
            request_data = {
                "file_url": test_case["url"],
                "filename": f"test_document_{i}.pdf"  # Optional filename override
            }
            
            print(f"📤 Sending URL: {test_case['url']}")
            
            response = requests.post(
                f"{BASE_URL}/parse-document",
                json=request_data,
                headers={
                    "X-API-Key": API_KEY,
                    "Content-Type": "application/json"
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Document parsing successful!")
                
                print(f"   • Source URL: {result.get('download_info', {}).get('source_url')}")
                print(f"   • Downloaded File: {result.get('download_info', {}).get('downloaded_filename')}")
                print(f"   • File Size: {result.get('download_info', {}).get('file_size_bytes', 0):,} bytes")
                print(f"   • Document Type: {result.get('document_metadata', {}).get('detected_document_type')}")
                print(f"   • Pages: {result.get('document_metadata', {}).get('total_pages')}")
                print(f"   • Content Blocks: {result.get('document_metadata', {}).get('total_content_blocks')}")
                
                # Save results
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                results_file = f'url_parsing_results_{i}_{timestamp}.json'
                with open(results_file, 'w') as f:
                    json.dump(result, f, indent=2)
                print(f"   💾 Results saved to: {results_file}")
                
            else:
                print(f"❌ Parsing failed with status code: {response.status_code}")
                print(f"   Error: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection failed. Make sure the server is running on http://localhost:8000")
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
        
        print()

def test_with_your_file_url():
    """Test with a custom URL - replace with your own file URL"""
    
    print("🧪 Testing with Custom File URL...")
    
    # Replace this with your actual file URL
    custom_url = input("Enter a file URL to test (or press Enter to skip): ").strip()
    
    if not custom_url:
        print("⏭️  Skipping custom URL test")
        return
    
    try:
        request_data = {
            "file_url": custom_url,
            "filename": "custom_document.pdf"
        }
        
        print(f"📤 Testing URL: {custom_url}")
        
        response = requests.post(
            f"{BASE_URL}/parse-document",
            json=request_data,
            headers={
                "X-API-Key": API_KEY,
                "Content-Type": "application/json"
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Custom URL parsing successful!")
            
            print(f"   • Downloaded File: {result.get('filename')}")
            print(f"   • File Size: {result.get('file_size_bytes', 0):,} bytes")
            print(f"   • Document Type: {result.get('document_metadata', {}).get('detected_document_type')}")
            
            # Save results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            results_file = f'custom_url_results_{timestamp}.json'
            with open(results_file, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"   💾 Results saved to: {results_file}")
            
        else:
            print(f"❌ Custom URL parsing failed with status: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Custom URL test failed: {str(e)}")

def test_health_check():
    """Quick health check"""
    print("🏥 Testing server health...")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Server is healthy! Document parsing: {result.get('document_parsing_configured')}")
            return True
        else:
            print(f"❌ Server health check failed: {response.status_code}")
            return False
    except:
        print("❌ Server is not running")
        return False

if __name__ == "__main__":
    print("🚀 Testing URL-based Document Parsing")
    print(f"🕐 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check server health first
    if test_health_check():
        print("\n" + "="*60)
        
        # Test with sample URLs
        test_parse_document_from_url()
        
        # Test with custom URL
        test_with_your_file_url()
        
        print("✨ All URL-based parsing tests completed!")
    else:
        print("⚠️  Server is not running. Please start the server first.")
    
    print(f"🕐 Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
