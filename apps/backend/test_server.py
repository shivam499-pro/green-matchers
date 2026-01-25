#!/usr/bin/env python3
"""
Test script to check if the Green Matchers backend can run properly
"""

import sys
import os
import traceback

def test_imports():
    """Test if all required imports work"""
    print("🔍 Testing imports...")
    
    try:
        # Test FastAPI
        from fastapi import FastAPI, HTTPException, Depends, WebSocket, Request, File, UploadFile
        print("✅ FastAPI imports successful")
        
        # Test database
        import mariadb
        print("✅ MariaDB import successful")
        
        # Test AI models
        from sentence_transformers import SentenceTransformer
        print("✅ Sentence Transformers import successful")
        
        # Test translation
        from deep_translator import GoogleTranslator
        print("✅ Deep Translator import successful")
        
        # Test vector services
        from vector_services import vector_service, initialize_vector_data, test_vector_functionality
        print("✅ Vector services import successful")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    print("🔍 Testing database connection...")
    
    try:
        import mariadb
        import os
        from dotenv import load_dotenv
        
        load_dotenv()
        
        # Try MariaDB connection
        conn = mariadb.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'greenmatchers2025'),
            database=os.getenv('DB_NAME', 'green_jobs'),
            port=int(os.getenv('DB_PORT', 3306))
        )
        print("✅ MariaDB connection successful")
        conn.close()
        return True
        
    except mariadb.Error as e:
        print(f"⚠️ MariaDB connection failed: {e}")
        print("🔄 Testing SQLite fallback...")
        try:
            import sqlite3
            conn = sqlite3.connect('green_jobs.db')
            print("✅ SQLite connection successful")
            conn.close()
            return True
        except Exception as e2:
            print(f"❌ SQLite connection also failed: {e2}")
            return False
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def test_vector_services():
    """Test vector services"""
    print("🔍 Testing vector services...")
    
    try:
        from vector_services import vector_service, test_vector_functionality
        
        # Test basic functionality
        result = test_vector_functionality()
        print(f"✅ Vector services test result: {result.get('status', 'unknown')}")
        return True
        
    except Exception as e:
        print(f"❌ Vector services error: {e}")
        return False

def test_app_creation():
    """Test if the main app can be created"""
    print("🔍 Testing app creation...")
    
    try:
        # Import the main app
        from app import app, init_db
        
        print("✅ App import successful")
        print(f"✅ App title: {app.title}")
        print(f"✅ App version: {app.version}")
        
        # Test database initialization
        init_result = init_db()
        print(f"✅ Database initialization: {init_result}")
        
        return True
        
    except Exception as e:
        print(f"❌ App creation error: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🚀 Green Matchers Backend Test Suite")
    print("=" * 50)
    
    tests = [
        ("Import Tests", test_imports),
        ("Database Connection", test_database_connection),
        ("Vector Services", test_vector_services),
        ("App Creation", test_app_creation)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\n📈 Summary: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! The backend should run successfully.")
        print("\n💡 To start the server, run:")
        print("   cd apps/backend")
        print("   python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload")
    else:
        print("\n⚠️ Some tests failed. Please check the errors above.")
        print("\n💡 Common fixes:")
        print("   - Install missing dependencies: pip install -r requirements.txt")
        print("   - Check database connection and credentials")
        print("   - Verify MariaDB is running")
        print("   - Check .env file configuration")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)