@echo off
echo Starting Amagara Masya System Setup...

:: Create and activate virtual environment if it doesn't exist
if not exist "backend\venv" (
    echo Creating virtual environment...
    python -m venv backend\venv
)

:: Activate virtual environment and install requirements
echo Activating virtual environment and installing requirements...
call backend\venv\Scripts\activate.bat
cd backend
pip install -r requirements.txt

:: Start Django server in a new window
echo Starting Django backend server...
start cmd /k "call venv\Scripts\activate.bat && python manage.py runserver"

:: Go back to root and start frontend server
cd ..
echo Starting Frontend server...
start cmd /k "cd frontend && python server.py"

echo System is starting up...
echo Backend will be available at: http://localhost:8000
echo Frontend will be available at: http://localhost:3000
echo.
echo Press any key to close this window...
pause > nul 