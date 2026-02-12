# PowerShell script to start both backend and frontend servers
# Usage: .\start.ps1

Write-Host "Starting Song Playlist App..." -ForegroundColor Green
Write-Host ""

# Check if backend venv exists
if (-not (Test-Path "backend\venv\Scripts\python.exe")) {
    Write-Host "ERROR: Backend virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run: cd backend && python -m venv venv && .\venv\Scripts\Activate.ps1 && pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

# Check if frontend node_modules exists
if (-not (Test-Path "frontend\node_modules")) {
    Write-Host "WARNING: Frontend dependencies not found. Installing..." -ForegroundColor Yellow
    Set-Location frontend
    npm install
    Set-Location ..
}

Write-Host "Starting Backend Server (Flask) on http://localhost:5000" -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\backend'; .\venv\Scripts\Activate.ps1; python app.py" -WindowStyle Normal

# Wait a bit for backend to start
Start-Sleep -Seconds 3

Write-Host "Starting Frontend Server (React) on http://localhost:3000" -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend'; npm start" -WindowStyle Normal

Write-Host ""
Write-Host "Both servers are starting in separate windows!" -ForegroundColor Green
Write-Host "   Backend:  http://localhost:5000" -ForegroundColor White
Write-Host "   Frontend: http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C in each window to stop the servers." -ForegroundColor Yellow

