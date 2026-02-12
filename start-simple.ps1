# Simple PowerShell script to start both servers
# Usage: .\start-simple.ps1

$backendPath = Join-Path $PSScriptRoot "backend"
$frontendPath = Join-Path $PSScriptRoot "frontend"

Write-Host "Starting Song Playlist App..." -ForegroundColor Green
Write-Host ""

# Start Backend
Write-Host "Starting Backend (Flask) on http://localhost:5000" -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; if (Test-Path 'venv\Scripts\Activate.ps1') { .\venv\Scripts\Activate.ps1; python app.py } else { Write-Host 'Virtual environment not found!'; pause }"

# Wait for backend to initialize
Start-Sleep -Seconds 2

# Start Frontend
Write-Host "Starting Frontend (React) on http://localhost:3000" -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendPath'; npm start"

Write-Host ""
Write-Host "Both servers are starting!" -ForegroundColor Green
Write-Host "   Backend:  http://localhost:5000" -ForegroundColor White
Write-Host "   Frontend: http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "Close the terminal windows or press Ctrl+C to stop." -ForegroundColor Yellow

