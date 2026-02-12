@echo off
REM Batch script to start both backend and frontend servers
REM Usage: start.bat

echo.
echo 🚀 Starting Song Playlist App...
echo.

REM Check if backend venv exists
if not exist "backend\venv\Scripts\python.exe" (
    echo ❌ Backend virtual environment not found!
    echo Please run: cd backend ^&^& python -m venv venv ^&^& venv\Scripts\activate.bat ^&^& pip install -r requirements.txt
    pause
    exit /b 1
)

REM Check if frontend node_modules exists
if not exist "frontend\node_modules" (
    echo ⚠️  Frontend dependencies not found. Installing...
    cd frontend
    call npm install
    cd ..
)

echo 📦 Starting Backend Server (Flask) on http://localhost:5000
start "Backend Server" cmd /k "cd /d %~dp0backend && venv\Scripts\activate.bat && python app.py"

REM Wait a bit for backend to start
timeout /t 3 /nobreak >nul

echo ⚛️  Starting Frontend Server (React) on http://localhost:3000
start "Frontend Server" cmd /k "cd /d %~dp0frontend && npm start"

echo.
echo ✅ Both servers are starting in separate windows!
echo    Backend:  http://localhost:5000
echo    Frontend: http://localhost:3000
echo.
echo Press Ctrl+C in each window to stop the servers.
echo.
pause

