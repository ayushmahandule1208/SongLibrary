# Song Playlist Dashboard

A full-stack application for managing and visualizing song playlists with data normalization, REST APIs, and an interactive dashboard.

## 🎯 Project Overview

This project processes song playlist data from JSON format, normalizes it, serves it through a REST API, and displays it in an interactive web dashboard with sorting, pagination, search, and data visualization features.

## 🛠️ Tech Stack

**Backend:**
- Python 3.8+
- Flask
- SQLite (or in-memory storage)
- Flask-CORS

**Frontend:**
- React
- JavaScript/ES6
- CSS

## 📋 Features

### Backend (Flask API)
- ✅ JSON data normalization and processing
- ✅ RESTful API endpoints
- ✅ Pagination support
- ✅ Search songs by title
- ✅ Star rating system (1-5 stars)
- ✅ CORS enabled

### Frontend (React Dashboard)
- ✅ Tabular data display with pagination (10 rows per page)
- ✅ Sortable columns (ascending/descending)
- ✅ Search functionality by song title
- ✅ CSV export
- ✅ Star rating for songs
- ✅ Data visualizations (scatter chart, histogram, bar charts)

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Node.js 14+ and npm
- Git

### Installation & Running

#### 1️⃣ Backend Setup
```bash
# Navigate to backend directory
cd song-playlist-app/backend

# Create and activate virtual environment
# Windows PowerShell:
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
```

Backend runs on: **http://localhost:5000**

#### 2️⃣ Frontend Setup

Open a new terminal window:
```bash
# Navigate to frontend directory
cd song-playlist-app/frontend

# Install dependencies
npm install

# Start the development server
npm start
```

Frontend runs on: **http://localhost:3000**

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/songs` | Get all songs (with pagination) |
| GET | `/api/songs?page=1&per_page=10` | Get paginated songs |
| GET | `/api/songs/search?title={title}` | Search song by title |
| POST | `/api/songs/{id}/rate` | Rate a song (1-5 stars) |
| GET | `/api/stats` | Get statistics |

## 📁 Project Structure
```
song-playlist-app/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   ├── data/              # JSON data files
│   └── instance/          # SQLite database
│
└── frontend/
    ├── src/
    │   ├── App.js         # Main React component
    │   ├── services/      # API service
    │   └── components/    # React components
    ├── package.json       # Node dependencies
    └── public/
```

## 🧪 Testing
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 🎨 Usage

1. **View All Songs**: The dashboard loads all songs on startup
2. **Sort Data**: Click any column header to sort
3. **Search**: Enter song title and click "Get Song"
4. **Rate Songs**: Click stars to rate (1-5)
5. **Export**: Click "Download CSV" to export data
6. **Visualizations**: Scroll down to view charts

## 🔧 Configuration

### Backend (.env - optional)
```
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key
```

### Frontend (.env - optional)
```
REACT_APP_API_URL=http://localhost:5000/api
```

## 📦 Dependencies

### Backend (requirements.txt)
```
Flask>=2.0.0
Flask-CORS>=3.0.0
pandas>=1.3.0
```

### Frontend (package.json)
```
react: ^18.0.0
axios: ^1.0.0
chart.js: ^3.0.0
react-chartjs-2: ^4.0.0
```

## 🐛 Troubleshooting

**Port conflicts:**
- Backend: Change port in `app.py`
- Frontend: Set `PORT=3001 npm start`

**Database reset:**
```bash
rm backend/instance/songs.db
```

