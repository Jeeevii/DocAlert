"""
Comprehensive test script for DocAlert API
Tests both voice call and document parsing endpoints
"""

import requests
import json
import os
from datetime import datetime

# Configuration
API_KEY = "2ZLp45FKyB9gVLLxeQGr6Om2qyAPltGI"
BASE_URL = "http://localhost:8000"
TEST_PHONE_NUMBER = "+15102586918"  # Your phone number from .env

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def test_health_check():
    """Test the health check endpoint"""
    print_section("🏥 HEALTH CHECK")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Health check successful!")
            print(f"   • Service: {result['service']}")
            print(f"   • Version: {result['version']}")
            print(f"   • Twilio Configured: {result['twilio_configured']}")
            print(f"   • Document Parsing: {result['document_parsing_configured']}")
            return True
        else:
            print(f"❌ Health check failed with status: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Make sure the server is running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Health check failed: {str(e)}")
        return False

def test_voice_call():
    """Test the voice call endpoint"""
    print_section("📞 VOICE CALL TEST")
    
    # Ask user if they want to make a real call
    make_call = input("Do you want to make a test call to your phone? (y/n): ").lower() == 'y'
    
    if not make_call:
        print("⏭️  Skipping voice call test (user declined)")
        return True
    
    try:
        call_data = {
            "to_number": TEST_PHONE_NUMBER,
            "message": f"Hello! This is a test call from your DocAlert system at {datetime.now().strftime('%I:%M %p')}. The voice calling feature is working correctly!"
        }
        
        response = requests.post(
            f"{BASE_URL}/make-call",
            json=call_data,
            headers={
                "X-API-Key": API_KEY,
                "Content-Type": "application/json"
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Voice call initiated successfully!")
            print(f"   • Call SID: {result.get('call_sid')}")
            print(f"   • Message: {result.get('message')}")
            print(f"   • Phone Number: {TEST_PHONE_NUMBER}")
            print("📱 Check your phone for the incoming call!")
            return True
        else:
            print(f"❌ Voice call failed with status: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Voice call test failed: {str(e)}")
        return False

def test_simple_call_endpoint():
    """Test the simplified /call endpoint"""
    print_section("📞 SIMPLE CALL ENDPOINT TEST")
    
    # Ask user if they want to make a real call
    make_call = input("Do you want to test the simple call endpoint? (y/n): ").lower() == 'y'
    
    if not make_call:
        print("⏭️  Skipping simple call test (user declined)")
        return True
    
    try:
        # Using form data for the simple endpoint
        call_data = {
            "phone_number": TEST_PHONE_NUMBER,
            "message": "This is a test of the simplified call endpoint. Everything is working great!"
        }
        
        response = requests.post(
            f"{BASE_URL}/call",
            data=call_data,  # Using form data instead of JSON
            headers={
                "X-API-Key": API_KEY
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Simple call endpoint successful!")
            print(f"   • Success: {result.get('success')}")
            print(f"   • Call SID: {result.get('call_sid')}")
            print(f"   • Message: {result.get('message')}")
            return True
        else:
            print(f"❌ Simple call failed with status: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Simple call test failed: {str(e)}")
        return False

def test_document_parsing():
    """Test the document parsing endpoint with URL"""
    print_section("📄 DOCUMENT PARSING TEST (URL)")
    
    # Test with a sample PDF URL
    test_url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
    
    try:
        request_data = {
            "file_url": test_url,
            "filename": "test_sample.pdf"
        }
        
        print(f"📤 Testing with URL: {test_url}")
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
            
            print("\n📊 Document Analysis Results:")
            if 'download_info' in result:
                download_info = result['download_info']
                print(f"   • Source URL: {download_info.get('source_url')}")
                print(f"   • Downloaded File: {download_info.get('downloaded_filename')}")
                print(f"   • File Size: {download_info.get('file_size_bytes', 0):,} bytes")
            
            print(f"   • File Type: {result.get('file_type')}")
            print(f"   • Extraction Method: {result.get('extraction_method')}")
            
            if 'document_metadata' in result:
                metadata = result['document_metadata']
                print(f"   • Document Type: {metadata.get('detected_document_type')}")
                print(f"   • Total Pages: {metadata.get('total_pages')}")
                print(f"   • Content Blocks: {metadata.get('total_content_blocks')}")
                print(f"   • Complexity Score: {metadata.get('complexity_score')}")
            
            if 'processing_instructions_for_llm' in result:
                instructions = result['processing_instructions_for_llm']
                print(f"   • LLM Approach: {instructions.get('suggested_approach')}")
                print(f"   • Key Areas: {', '.join(instructions.get('key_areas_to_focus', [])[:3])}...")
            
            # Save detailed results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            results_file = f'comprehensive_parsing_results_{timestamp}.json'
            with open(results_file, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\n💾 Detailed results saved to: {results_file}")
            
            return True
            
        else:
            print(f"❌ Document parsing failed with status: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Document parsing test failed: {str(e)}")
        return False

def test_llm_parsing_endpoint():
    """Test the LLM parsing test endpoint"""
    print_section("🤖 LLM PARSING TEST ENDPOINT")
    
    try:
        response = requests.post(
            f"{BASE_URL}/test-llm-parsing",
            headers={
                "X-API-Key": API_KEY,
                "Content-Type": "application/json"
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ LLM parsing test successful!")
            print(f"   • Status: {result['test_status']}")
            print(f"   • Message: {result['message']}")
            
            if 'parsing_result' in result:
                parsing_result = result['parsing_result']
                metadata = parsing_result.get('document_metadata', {})
                print(f"   • Document Type: {metadata.get('detected_document_type', 'Unknown')}")
                print(f"   • Pages Analyzed: {metadata.get('total_pages', 0)}")
            
            return True
        else:
            print(f"❌ LLM parsing test failed with status: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ LLM parsing test failed: {str(e)}")
        return False

def test_document_templates():
    """Test the document templates endpoint"""
    print_section("📋 DOCUMENT TEMPLATES")
    
    try:
        response = requests.get(
            f"{BASE_URL}/document-templates",
            headers={"X-API-Key": API_KEY}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Document templates retrieved successfully!")
            print(f"   • Available Templates: {list(result.get('templates', {}).keys())}")
            print(f"   • Supported Field Types: {result.get('supported_field_types', [])}")
            print(f"   • Supported File Types: {result.get('supported_file_types', [])}")
            return True
        else:
            print(f"❌ Document templates failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Document templates test failed: {str(e)}")
        return False

def run_all_tests():
    """Run all tests and provide a summary"""
    print("🚀 Starting DocAlert API Comprehensive Tests")
    print(f"🕐 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Track test results
    tests = [
        ("Health Check", test_health_check),
        ("Document Templates", test_document_templates),
        ("Document Parsing", test_document_parsing),
        ("LLM Parsing Test", test_llm_parsing_endpoint),
        ("Voice Call", test_voice_call),
        ("Simple Call Endpoint", test_simple_call_endpoint)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {str(e)}")
            results[test_name] = False
    
    # Print summary
    print_section("📊 TEST SUMMARY")
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✅ PASSED" if passed_test else "❌ FAILED"
        print(f"   {test_name}: {status}")
    
    print(f"\n🎯 Overall Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your DocAlert API is working perfectly!")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    print(f"🕐 Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    run_all_tests()
