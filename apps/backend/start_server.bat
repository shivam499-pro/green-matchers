@echo off
echo 🚀 Starting Green Matchers Backend Server...
echo ===========================================

cd /d "apps/backend"

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo ✅ Virtual environment found
    call venv\Scripts\activate.bat
) else (
    echo ⚠️ Virtual environment not found, using system Python
)

REM Start the server
echo 🌐 Starting server on http://localhost:8000
echo 📁 API docs available at http://localhost:8000/docs
echo 🔧 Use Ctrl+C to stop the server

python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload

echo.
echo ❌ Server stopped
pause