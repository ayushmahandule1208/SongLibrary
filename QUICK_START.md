# 🚀 Quick Start - Single Command

You can now run both backend and frontend with a single command!

## Option 1: Using PowerShell Script (Recommended for Windows)

```powershell
.\start.ps1
```

This will open two separate terminal windows - one for backend and one for frontend.

## Option 2: Using Batch File (Windows)

```cmd
start.bat
```

## Option 3: Using npm (Cross-platform)

First, install the root dependencies:
```bash
npm install
```

Then run:
```bash
npm start
```

This will run both servers in a single terminal with colored output.

## Option 4: Using Bash Script (macOS/Linux)

```bash
chmod +x start.sh
./start.sh
```

---

## 📝 First Time Setup

If you haven't set up the project yet:

1. **Install root dependencies** (for npm start option):
   ```bash
   npm install
   ```

2. **Backend setup** (if not already done):
   ```bash
   cd backend
   python -m venv venv
   .\venv\Scripts\Activate.ps1  # Windows PowerShell
   # or: venv\Scripts\activate.bat  # Windows CMD
   # or: source venv/bin/activate  # macOS/Linux
   pip install -r requirements.txt
   cd ..
   ```

3. **Frontend setup** (if not already done):
   ```bash
   cd frontend
   npm install
   cd ..
   ```

---

## 🎯 What Happens When You Run

- **Backend** starts on: http://localhost:5000
- **Frontend** starts on: http://localhost:3000 (opens automatically)

Both servers will run until you stop them (Ctrl+C).

---

## 🛑 Stopping the Servers

- **PowerShell/Batch scripts**: Close the terminal windows or press Ctrl+C in each
- **npm start**: Press Ctrl+C once to stop both servers
- **Bash script**: Press Ctrl+C to stop both servers

---

## 💡 Recommended Method

For **Windows users**, I recommend using the **PowerShell script** (`.\start.ps1`) as it:
- Opens separate windows for each server (easier to see logs)
- Automatically checks for dependencies
- Provides clear status messages

For **cross-platform** or if you prefer a single terminal, use **npm start** (after running `npm install` in the root directory).

