# 🚨 Green Matchers Backend Troubleshooting Guide

## 📋 Problem Summary
You were experiencing issues running your Green Matchers backend code. I've identified and fixed the following problems:

## 🔧 Issues Fixed

### 1. **Database Connection Password Mismatch**
- **Problem**: `test_connection.py` was using password `"Shivam12345"` but `.env` file had `"greenmatchers2025"`
- **Fix**: Updated `test_connection.py` to use the correct password from `.env` file

### 2. **Import Organization and Error Handling**
- **Problem**: Import statements were disorganized and could cause import errors
- **Fix**: Reorganized imports in `app.py` with better error handling for AI services

### 3. **Missing Dependencies**
- **Problem**: Some AI services might not be available
- **Fix**: Added graceful fallbacks when AI services fail to import

## 🧪 Testing

### Run the Test Suite
```bash
# Navigate to backend directory
cd apps/backend

# Run the comprehensive test
python test_server.py
```

### Expected Output
If everything is working correctly, you should see:
```
🚀 Green Matchers Backend Test Suite
==================================================
📋 Running Import Tests...
✅ FastAPI imports successful
✅ MariaDB import successful
✅ Sentence Transformers import successful
✅ Deep Translator import successful
✅ Vector services import successful

📋 Running Database Connection...
✅ MariaDB connection successful

📋 Running Vector Services...
✅ Vector services test result: success

📋 Running App Creation...
✅ App import successful
✅ App title: Green Matchers API - PRODUCTION
✅ App version: 4.0.0
✅ Database initialization: True

==================================================
📊 TEST RESULTS SUMMARY
==================================================
Import Tests: ✅ PASS
Database Connection: ✅ PASS
Vector Services: ✅ PASS
App Creation: ✅ PASS

📈 Summary: 4 passed, 0 failed

🎉 ALL TESTS PASSED! The backend should run successfully.

💡 To start the server, run:
   cd apps/backend
   python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

## 🚀 Starting the Server

### Option 1: Using the Batch File (Recommended for Windows)
```bash
# Double-click: apps/backend/start_server.bat
# OR run from command line:
cd apps/backend
start_server.bat
```

### Option 2: Manual Command
```bash
cd apps/backend
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### Option 3: Using PowerShell (Fixed)
```powershell
cd apps/backend
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

## 🌐 Server Information

Once running, your server will be available at:
- **Main API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🔍 Common Issues and Solutions

### Issue 1: Import Errors
**Error**: `ModuleNotFoundError: No module named 'some_module'`
**Solution**: Install missing dependencies
```bash
cd apps/backend
pip install -r requirements.txt
```

### Issue 2: Database Connection Failed
**Error**: `Can't connect to MySQL server`
**Solutions**:
1. Check if MariaDB/MySQL is running
2. Verify credentials in `.env` file
3. Check if database `green_jobs` exists
4. Try SQLite fallback (automatic)

### Issue 3: Port Already in Use
**Error**: `Address already in use`
**Solution**: Change port in startup command
```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8001 --reload
```

### Issue 4: Virtual Environment Issues
**Error**: `Module not found` even after pip install
**Solution**: Activate virtual environment
```bash
cd apps/backend
venv\Scripts\activate
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

## 📊 Available Endpoints

### Core API Endpoints
- `GET /health` - Server health check
- `GET /stats` - System statistics
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/jobs/search` - Job search with AI
- `POST /api/career/recommendations` - Career recommendations
- `POST /api/translate` - Multi-language translation

### AI-Powered Endpoints
- `POST /api/vector/jobs/semantic-search` - AI semantic job search
- `POST /api/vector/careers/semantic-recommendations` - AI career matching
- `POST /api/ai/resume/analyze` - Resume analysis
- `POST /api/ai/salary/predict` - Salary prediction

### Multi-Language Support
- **10 Languages**: English, Hindi, Bengali, Telugu, Tamil, Marathi, Gujarati, Kannada, Malayalam, Odia
- `POST /api/translate` - Single text translation
- `POST /api/translate/batch` - Batch translation

## 🎯 Hackathon Features

Your backend includes these advanced features:
- ✅ **MariaDB Vector Search** - Database-native AI operations
- ✅ **Multi-Language AI** - 10 Indian languages supported
- ✅ **Semantic Search** - AI-powered job and career matching
- ✅ **Real-time Analytics** - Live market demand scoring
- ✅ **Resume Analysis** - AI-powered skill extraction
- ✅ **Salary Prediction** - ML-based compensation forecasting

## 📞 Need Help?

If you're still experiencing issues:

1. **Run the test suite** first: `python test_server.py`
2. **Check the error messages** - they usually indicate the specific problem
3. **Verify your environment**:
   - Python version (3.8+ recommended)
   - MariaDB/MySQL running
   - Required dependencies installed
   - `.env` file properly configured

4. **Common fixes**:
   - Restart your terminal/command prompt
   - Reinstall dependencies: `pip install -r requirements.txt`
   - Check MariaDB service is running
   - Verify database credentials

## 🎉 Success!

Your Green Matchers backend should now be working properly with:
- ✅ Fixed database connections
- ✅ Proper import handling
- ✅ AI services with fallbacks
- ✅ Multi-language support
- ✅ Vector search capabilities
- ✅ Comprehensive error handling

The backend is ready for your hackathon presentation! 🚀