Write-Host "Starting Amagara Masya System Setup..." -ForegroundColor Green

# Create and activate virtual environment if it doesn't exist
if (-not (Test-Path "backend\venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv backend\venv
}

# Activate virtual environment and install requirements
Write-Host "Activating virtual environment and installing requirements..." -ForegroundColor Yellow
& backend\venv\Scripts\Activate.ps1
Set-Location backend

# Install core dependencies first
Write-Host "Installing core dependencies..." -ForegroundColor Yellow
pip install --upgrade pip
pip install Django==4.2.10 djangorestframework==3.14.0 djangorestframework-simplejwt==5.3.1 django-cors-headers==4.3.1

# Try to install Pillow using a wheel
Write-Host "Installing Pillow..." -ForegroundColor Yellow
pip install --only-binary :all: Pillow==9.5.0

# Install remaining requirements
Write-Host "Installing remaining requirements..." -ForegroundColor Yellow
pip install django-filter==23.5 python-dotenv==1.0.1 django-storages==1.14.2 boto3==1.28.62 django-allauth==0.57.0 django-crispy-forms==2.0 crispy-bootstrap5==2023.10 django-environ==0.11.2 django-phonenumber-field==7.1.0 phonenumbers==8.13.22 django-import-export==3.3.0 django-report-builder==7.0.0

# Start Django server in a new window
Write-Host "Starting Django backend server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& {Set-Location '$PWD'; & venv\Scripts\Activate.ps1; python manage.py runserver}"

# Go back to root and start frontend server
Set-Location ..
Write-Host "Starting Frontend server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& {Set-Location '$PWD\frontend'; python server.py}"

Write-Host "`nSystem is starting up..." -ForegroundColor Green
Write-Host "Backend will be available at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend will be available at: http://localhost:3000" -ForegroundColor Cyan
Write-Host "`nPress any key to close this window..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 