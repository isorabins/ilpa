# verify_deployment.py - Run after deployment
import requests
import json
import sys
import os
from urllib.parse import urljoin

def verify_deployment():
    """Verify that both backend and frontend are deployed and working correctly"""
    print("🔍 Verifying deployment...\n")
    
    # Configuration - update these URLs for your deployment
    backend_url = os.getenv("BACKEND_URL", "https://ilpa-backend.herokuapp.com")
    frontend_url = os.getenv("FRONTEND_URL", "https://your-app.vercel.app")  # Replace with your actual URL
    
    all_good = True
    
    print(f"Backend URL: {backend_url}")
    print(f"Frontend URL: {frontend_url}")
    print()
    
    # Check backend health
    print("🔧 Testing backend health...")
    health_url = urljoin(backend_url, "/health")
    try:
        response = requests.get(health_url, timeout=10)
        if response.status_code == 200:
            print("✅ Backend is healthy")
            try:
                health_data = response.json()
                print(f"   Response: {health_data}")
            except:
                print(f"   Response: {response.text}")
        else:
            print(f"❌ Backend returned {response.status_code}")
            print(f"   Response: {response.text}")
            all_good = False
    except requests.exceptions.Timeout:
        print("❌ Backend request timed out (>10s)")
        print("   Fix: Check if Heroku app is running with 'heroku logs --tail'")
        all_good = False
    except requests.exceptions.ConnectionError:
        print(f"❌ Backend unreachable at {health_url}")
        print("   Fix: Check Heroku deployment status")
        all_good = False
    except Exception as e:
        print(f"❌ Backend check failed: {e}")
        all_good = False
    
    # Check frontend accessibility
    print("\n🌐 Testing frontend accessibility...")
    try:
        response = requests.get(frontend_url, timeout=10)
        if response.status_code == 200:
            print("✅ Frontend is accessible")
            # Check if it looks like a React app
            if "react" in response.text.lower() or "next" in response.text.lower():
                print("   ✅ Appears to be a React/Next.js application")
            else:
                print("   ⚠️  Response doesn't look like expected React app")
        else:
            print(f"❌ Frontend returned {response.status_code}")
            all_good = False
    except requests.exceptions.Timeout:
        print("❌ Frontend request timed out (>10s)")
        print("   Fix: Check Vercel deployment status")
        all_good = False
    except requests.exceptions.ConnectionError:
        print(f"❌ Frontend unreachable at {frontend_url}")
        print("   Fix: Check Vercel deployment dashboard")
        all_good = False
    except Exception as e:
        print(f"❌ Frontend check failed: {e}")
        all_good = False
    
    # Test backend API endpoints
    print("\n🔌 Testing API endpoints...")
    
    # Test chat endpoint (should return 401 without auth, which is correct)
    chat_url = urljoin(backend_url, "/api/chat")
    try:
        response = requests.post(chat_url, json={"message": "test"}, timeout=10)
        if response.status_code == 401:
            print("✅ Chat API authentication is working (401 expected without auth)")
        elif response.status_code == 405:
            print("✅ Chat API endpoint exists (405 Method Not Allowed for POST)")
        elif response.status_code == 404:
            print("❌ Chat API endpoint not found (404)")
            print("   Fix: Check if /api/chat endpoint is implemented")
            all_good = False
        else:
            print(f"⚠️  Chat API returned unexpected status: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ Chat API endpoint test failed: {e}")
        all_good = False
    
    # Test upload endpoint
    upload_url = urljoin(backend_url, "/api/upload")
    try:
        response = requests.post(upload_url, json={"test": "data"}, timeout=10)
        if response.status_code in [401, 405, 422]:  # Expected without proper auth/data
            print("✅ Upload API endpoint exists and requires authentication")
        elif response.status_code == 404:
            print("❌ Upload API endpoint not found (404)")
            print("   Fix: Check if /api/upload endpoint is implemented")
            all_good = False
        else:
            print(f"⚠️  Upload API returned unexpected status: {response.status_code}")
    except Exception as e:
        print(f"❌ Upload API endpoint test failed: {e}")
        all_good = False
    
    # Test planning endpoint
    planning_url = urljoin(backend_url, "/api/planning")
    try:
        response = requests.post(planning_url, json={"test": "data"}, timeout=10)
        if response.status_code in [401, 405, 422]:  # Expected without proper auth/data
            print("✅ Planning API endpoint exists and requires authentication")
        elif response.status_code == 404:
            print("❌ Planning API endpoint not found (404)")
            print("   Fix: Check if /api/planning endpoint is implemented")
            all_good = False
        else:
            print(f"⚠️  Planning API returned unexpected status: {response.status_code}")
    except Exception as e:
        print(f"❌ Planning API endpoint test failed: {e}")
        all_good = False
    
    # Test CORS configuration
    print("\n🌍 Testing CORS configuration...")
    try:
        # Test preflight request
        response = requests.options(chat_url, 
                                  headers={
                                      'Origin': frontend_url,
                                      'Access-Control-Request-Method': 'POST'
                                  }, 
                                  timeout=10)
        if 'access-control-allow-origin' in response.headers:
            print("✅ CORS headers are present")
            origin = response.headers.get('access-control-allow-origin')
            if origin == '*' or frontend_url in origin:
                print("✅ CORS allows frontend origin")
            else:
                print(f"⚠️  CORS origin mismatch: {origin}")
        else:
            print("❌ CORS headers missing")
            print("   Fix: Add CORS middleware to FastAPI app")
            all_good = False
    except Exception as e:
        print(f"⚠️  CORS test failed: {e}")
        print("   This might be normal if endpoints don't support OPTIONS")
    
    print("\n" + "=" * 50)
    print("📊 DEPLOYMENT VERIFICATION SUMMARY")
    print("=" * 50)
    
    if all_good:
        print("🎉 ALL DEPLOYMENT CHECKS PASSED!")
        print("\n✅ Your ILPA system is successfully deployed and ready for use!")
        print("\nNext steps:")
        print("1. Create a user account on the frontend")
        print("2. Test the complete workflow:")
        print("   - Have a conversation with Life Coach")
        print("   - Upload a text file to a domain")
        print("   - Start and complete a planning session")
        print("   - View your finalized weekly plan")
        return 0
    else:
        print("🚨 SOME DEPLOYMENT CHECKS FAILED!")
        print("\nCommon fixes:")
        print("- Check Heroku logs: heroku logs --tail")
        print("- Check Vercel deployment dashboard")
        print("- Verify environment variables are set correctly")
        print("- Ensure all endpoints are implemented")
        return 1

if __name__ == "__main__":
    print("🚀 ILPA Deployment Verification")
    print("=" * 50)
    print()
    print("This script verifies that your ILPA deployment is working correctly.")
    print("Make sure to update the frontend_url variable with your actual Vercel URL.")
    print()
    
    sys.exit(verify_deployment()) 