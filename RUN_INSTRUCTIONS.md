# How to Run the Song Playlist App

This guide will help you run both the backend (Flask) and frontend (React) applications.

## Prerequisites

- **Python 3.8+** (Python 3.12 is being used based on venv)
- **Node.js 14+** and npm
- **Git** (if cloning the repository)

---

## 🐍 Backend Setup (Flask)

### Step 1: Navigate to Backend Directory
```bash
cd song-playlist-app/backend
```

### Step 2: Activate Virtual Environment

**On Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

### Step 3: Install Dependencies (if not already installed)
```bash
pip install -r requirements.txt
```

### Step 4: Run the Backend Server
```bash
python app.py
```

The backend will start on **http://localhost:5000**

You should see:
```
Starting Flask application...
App created. Debug mode: True
Starting server on http://0.0.0.0:5000
```

**Keep this terminal window open!**

---

## ⚛️ Frontend Setup (React)

### Step 1: Open a NEW Terminal Window

Keep the backend running in the first terminal, and open a new terminal window.

### Step 2: Navigate to Frontend Directory
```bash
cd song-playlist-app/frontend
```

### Step 3: Install Dependencies (if not already installed)
```bash
npm install
```

### Step 4: Run the Frontend Development Server
```bash
npm start
```

The frontend will start on **http://localhost:3000** and should automatically open in your browser.

**Keep this terminal window open too!**

---

## 🚀 Quick Start (Both Servers)

If you want to run both servers quickly, you can use two terminal windows:

### Terminal 1 - Backend:
```bash
cd song-playlist-app/backend
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# or: venv\Scripts\activate.bat  # Windows CMD
# or: source venv/bin/activate  # macOS/Linux
python app.py
```

### Terminal 2 - Frontend:
```bash
cd song-playlist-app/frontend
npm start
```

---

## ✅ Verification

Once both servers are running:

1. **Backend API**: Visit http://localhost:5000/api/stats (should return JSON)
2. **Frontend App**: Visit http://localhost:3000 (should show the Playlist Dashboard)

---

## 🔧 Troubleshooting

### Backend Issues:

**Port 5000 already in use:**
- Find and close the process using port 5000, or
- Change the port in `backend/app.py` (line 411) and update `frontend/src/services/api.js` (line 3)

**Virtual environment not found:**
```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
```

**Database issues:**
- The database will be created automatically in `backend/instance/songs.db`
- If you need to reset, delete `backend/instance/songs.db` and restart the backend

### Frontend Issues:

**Port 3000 already in use:**
- React will ask if you want to use a different port (usually 3001)
- Or change the port: `set PORT=3001 && npm start` (Windows) or `PORT=3001 npm start` (macOS/Linux)

**Dependencies not installed:**
```bash
cd frontend
npm install
```

**API connection errors:**
- Make sure the backend is running on port 5000
- Check `frontend/src/services/api.js` - it should point to `http://localhost:5000/api`
- You can set a custom API URL with environment variable: `REACT_APP_API_URL=http://localhost:5000/api`

---

## 📝 Environment Variables (Optional)

### Backend (.env file in backend/ directory):
```
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env file in frontend/ directory):
```
REACT_APP_API_URL=http://localhost:5000/api
```

---

## 🛑 Stopping the Servers

- **Backend**: Press `Ctrl+C` in the backend terminal
- **Frontend**: Press `Ctrl+C` in the frontend terminal

---

## 📦 Production Build

### Frontend Production Build:
```bash
cd frontend
npm run build
```

This creates an optimized production build in the `frontend/build/` directory.

---

## 🎯 Default Ports

- **Backend**: http://localhost:5000
- **Frontend**: http://localhost:3000
- **API Base URL**: http://localhost:5000/api

---

Happy coding! 🎵

